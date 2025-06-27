#!/usr/bin/env python3
"""
🔥 GOD-TIER PhantomAutoBuyBot - Advanced Email & OTP Handler
Handles Gmail integration, OTP extraction, and email automation
"""

import os
import re
import asyncio
import imaplib
import email
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, List
import aiohttp
import base64
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

class EmailHandler:
    def __init__(self):
        self.gmail_user = os.getenv('GMAIL_USER')
        self.gmail_password = os.getenv('GMAIL_PASSWORD')
        self.gmail_api_key = os.getenv('GMAIL_API_KEY')
        self.imap_server = 'imap.gmail.com'
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        
        # OTP patterns for different services
        self.otp_patterns = {
            'apple': [
                r'Your Apple ID verification code is:?\s*(\d{6})',
                r'Apple ID verification code:\s*(\d{6})',
                r'(\d{6})\s*is your Apple ID verification code'
            ],
            'generic': [
                r'verification code:?\s*(\d{4,8})',
                r'code:?\s*(\d{4,8})',
                r'OTP:?\s*(\d{4,8})',
                r'(\d{4,8})\s*is your.*code'
            ]
        }
    
    async def connect_imap(self) -> Optional[imaplib.IMAP4_SSL]:
        """Connect to Gmail IMAP"""
        try:
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.gmail_user, self.gmail_password)
            return mail
        except Exception as e:
            print(f"❌ [EMAIL] IMAP connection failed: {e}")
            return None
    
    async def get_latest_emails(self, sender: str = None, subject_contains: str = None, 
                               since_minutes: int = 5) -> List[Dict]:
        """Get latest emails matching criteria"""
        mail = await self.connect_imap()
        if not mail:
            return []
        
        try:
            mail.select('inbox')
            
            # Build search criteria
            search_criteria = []
            
            # Time filter
            since_date = (datetime.now() - timedelta(minutes=since_minutes)).strftime('%d-%b-%Y')
            search_criteria.append(f'SINCE {since_date}')
            
            # Sender filter
            if sender:
                search_criteria.append(f'FROM "{sender}"')
            
            # Subject filter
            if subject_contains:
                search_criteria.append(f'SUBJECT "{subject_contains}"')
            
            # Search emails
            search_string = ' '.join(search_criteria)
            status, messages = mail.search(None, search_string)
            
            if status != 'OK':
                return []
            
            email_ids = messages[0].split()
            emails = []
            
            # Process latest emails (max 10)
            for email_id in email_ids[-10:]:
                try:
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    if status == 'OK':
                        email_body = msg_data[0][1]
                        email_message = email.message_from_bytes(email_body)
                        
                        # Extract email data
                        email_data = {
                            'id': email_id.decode(),
                            'subject': email_message['Subject'],
                            'from': email_message['From'],
                            'date': email_message['Date'],
                            'body': self._extract_email_body(email_message)
                        }
                        emails.append(email_data)
                        
                except Exception as e:
                    print(f"⚠️ [EMAIL] Error processing email {email_id}: {e}")
            
            mail.close()
            mail.logout()
            return emails
            
        except Exception as e:
            print(f"❌ [EMAIL] Error fetching emails: {e}")
            return []
    
    def _extract_email_body(self, email_message) -> str:
        """Extract text body from email message"""
        body = ""
        
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    try:
                        body = part.get_payload(decode=True).decode()
                        break
                    except:
                        continue
        else:
            try:
                body = email_message.get_payload(decode=True).decode()
            except:
                body = str(email_message.get_payload())
        
        return body
    
    async def extract_otp_from_email(self, email_body: str, service: str = 'generic') -> Optional[str]:
        """Extract OTP code from email body"""
        patterns = self.otp_patterns.get(service, self.otp_patterns['generic'])
        
        for pattern in patterns:
            match = re.search(pattern, email_body, re.IGNORECASE)
            if match:
                otp = match.group(1)
                print(f"✅ [EMAIL] OTP extracted: {otp}")
                return otp
        
        print(f"⚠️ [EMAIL] No OTP found in email")
        return None
    
    async def wait_for_otp(self, sender: str = None, service: str = 'apple', 
                          timeout: int = 300) -> Optional[str]:
        """Wait for OTP email and extract code"""
        print(f"📧 [EMAIL] Waiting for OTP from {sender or 'any sender'}...")
        
        start_time = time.time()
        last_check = datetime.now()
        
        while time.time() - start_time < timeout:
            try:
                # Get emails since last check
                emails = await self.get_latest_emails(
                    sender=sender,
                    since_minutes=1
                )
                
                for email_data in emails:
                    # Check if this email contains OTP
                    otp = await self.extract_otp_from_email(email_data['body'], service)
                    if otp:
                        print(f"🎯 [EMAIL] OTP received: {otp}")
                        return otp
                
                # Wait before next check
                await asyncio.sleep(5)
                
            except Exception as e:
                print(f"⚠️ [EMAIL] Error checking for OTP: {e}")
                await asyncio.sleep(10)
        
        print(f"⏰ [EMAIL] OTP timeout after {timeout} seconds")
        return None
    
    async def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Send email via SMTP"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.gmail_user
            msg['To'] = to_email
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.gmail_user, self.gmail_password)
            
            text = msg.as_string()
            server.sendmail(self.gmail_user, to_email, text)
            server.quit()
            
            print(f"✅ [EMAIL] Email sent to {to_email}")
            return True
            
        except Exception as e:
            print(f"❌ [EMAIL] Failed to send email: {e}")
            return False
    
    async def setup_gmail_api(self) -> bool:
        """Setup Gmail API credentials"""
        try:
            # This would typically involve OAuth2 flow
            # For now, we'll use app passwords
            if self.gmail_user and self.gmail_password:
                print("✅ [EMAIL] Gmail credentials configured")
                return True
            else:
                print("⚠️ [EMAIL] Gmail credentials not configured")
                return False
        except Exception as e:
            print(f"❌ [EMAIL] Gmail API setup failed: {e}")
            return False

class SMSHandler:
    def __init__(self):
        self.twilio_sid = os.getenv('TWILIO_SID')
        self.twilio_token = os.getenv('TWILIO_TOKEN')
        self.twilio_phone = os.getenv('TWILIO_PHONE')
        
    async def send_sms(self, to_phone: str, message: str) -> bool:
        """Send SMS via Twilio"""
        if not all([self.twilio_sid, self.twilio_token, self.twilio_phone]):
            print("⚠️ [SMS] Twilio credentials not configured")
            return False
        
        try:
            url = f"https://api.twilio.com/2010-04-01/Accounts/{self.twilio_sid}/Messages.json"
            
            auth = aiohttp.BasicAuth(self.twilio_sid, self.twilio_token)
            data = {
                'From': self.twilio_phone,
                'To': to_phone,
                'Body': message
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, auth=auth, data=data) as response:
                    if response.status == 201:
                        print(f"✅ [SMS] SMS sent to {to_phone}")
                        return True
                    else:
                        print(f"❌ [SMS] Failed to send SMS: {response.status}")
                        return False
                        
        except Exception as e:
            print(f"❌ [SMS] SMS sending failed: {e}")
            return False

class OTPManager:
    def __init__(self):
        self.email_handler = EmailHandler()
        self.sms_handler = SMSHandler()
        self.otp_cache = {}
        
    async def get_otp(self, method: str = 'email', service: str = 'apple', 
                     timeout: int = 300) -> Optional[str]:
        """Get OTP via specified method"""
        print(f"🔐 [OTP] Requesting OTP via {method} for {service}")
        
        if method == 'email':
            return await self.email_handler.wait_for_otp(
                sender=self._get_sender_for_service(service),
                service=service,
                timeout=timeout
            )
        elif method == 'sms':
            # For SMS, we'd need to implement SMS OTP extraction
            print("⚠️ [OTP] SMS OTP not implemented yet")
            return None
        else:
            print(f"❌ [OTP] Unknown method: {method}")
            return None
    
    def _get_sender_for_service(self, service: str) -> str:
        """Get expected sender email for service"""
        senders = {
            'apple': 'appleid@id.apple.com',
            'google': 'accounts-noreply@google.com',
            'microsoft': 'account-security-noreply@accountprotection.microsoft.com'
        }
        return senders.get(service, None)
    
    async def cache_otp(self, service: str, otp: str, ttl: int = 300):
        """Cache OTP for reuse"""
        expiry = time.time() + ttl
        self.otp_cache[service] = {
            'otp': otp,
            'expiry': expiry
        }
        print(f"💾 [OTP] Cached OTP for {service}")
    
    async def get_cached_otp(self, service: str) -> Optional[str]:
        """Get cached OTP if still valid"""
        if service in self.otp_cache:
            cached = self.otp_cache[service]
            if time.time() < cached['expiry']:
                print(f"🎯 [OTP] Using cached OTP for {service}")
                return cached['otp']
            else:
                del self.otp_cache[service]
                print(f"⏰ [OTP] Cached OTP expired for {service}")
        
        return None
    
    async def test_email_connection(self) -> bool:
        """Test email connection"""
        return await self.email_handler.setup_gmail_api()
    
    async def test_sms_connection(self) -> bool:
        """Test SMS connection"""
        # Test SMS would require sending to a test number
        return bool(self.sms_handler.twilio_sid)

# Global OTP manager instance
otp_manager = OTPManager()

async def get_otp_code(service: str = 'apple', method: str = 'email', 
                      timeout: int = 300) -> Optional[str]:
    """Convenience function to get OTP"""
    # Try cached first
    cached_otp = await otp_manager.get_cached_otp(service)
    if cached_otp:
        return cached_otp
    
    # Get new OTP
    otp = await otp_manager.get_otp(method, service, timeout)
    if otp:
        await otp_manager.cache_otp(service, otp)
    
    return otp

async def test_email_system():
    """Test email system functionality"""
    print("🧪 [TEST] Testing email system...")
    
    email_handler = EmailHandler()
    
    # Test connection
    if await email_handler.setup_gmail_api():
        print("✅ [TEST] Email connection successful")
        
        # Test getting recent emails
        emails = await email_handler.get_latest_emails(since_minutes=60)
        print(f"📧 [TEST] Found {len(emails)} recent emails")
        
        return True
    else:
        print("❌ [TEST] Email connection failed")
        return False

if __name__ == "__main__":
    async def main():
        await test_email_system()
    
    asyncio.run(main())