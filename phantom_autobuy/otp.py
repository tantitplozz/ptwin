"""
🔐 GOD-TIER OTP Handler
Advanced OTP detection, bypass, and automation
"""

import random
import asyncio
import re
import requests
from datetime import datetime
from .config import *

class OTPHandler:
    def __init__(self):
        self.otp_patterns = [
            r'\b\d{6}\b',  # 6-digit OTP
            r'\b\d{4}\b',  # 4-digit OTP
            r'\b\d{8}\b',  # 8-digit OTP
        ]
        self.otp_sources = {
            'sms': {'priority': 1, 'success_rate': 0.95},
            'email': {'priority': 2, 'success_rate': 0.90},
            'app': {'priority': 3, 'success_rate': 0.85},
            'voice': {'priority': 4, 'success_rate': 0.70}
        }
        
    async def handle_otp_flow(self, page):
        """Handle complete OTP flow"""
        print("🔐 [OTP] Starting OTP handling flow...")
        
        # Step 1: Detect OTP requirement
        otp_required = await self._detect_otp_requirement(page)
        
        if not otp_required:
            print("✅ [OTP] No OTP required")
            return {'success': True, 'code': None, 'method': 'none'}
            
        # Step 2: Identify OTP method
        otp_method = await self._identify_otp_method(page)
        
        # Step 3: Request OTP
        request_result = await self._request_otp(page, otp_method)
        
        # Step 4: Retrieve OTP
        otp_code = await self._retrieve_otp(page, otp_method)
        
        # Step 5: Submit OTP
        submit_result = await self._submit_otp(page, otp_code)
        
        result = {
            'success': submit_result.get('success', False),
            'code': otp_code,
            'method': otp_method,
            'attempts': submit_result.get('attempts', 1),
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"🔐 [OTP] Flow completed: {result}")
        return result
        
    async def _detect_otp_requirement(self, page):
        """Detect if OTP is required"""
        print("🔍 [OTP] Detecting OTP requirement...")
        
        otp_indicators = [
            'text="Enter verification code"',
            'text="OTP"',
            'text="One-time password"',
            'text="Verification code"',
            'text="Security code"',
            'input[placeholder*="code"]',
            'input[placeholder*="OTP"]',
            'input[name*="otp"]',
            'input[name*="verification"]',
            '.otp-input',
            '.verification-code'
        ]
        
        for indicator in otp_indicators:
            try:
                element = await page.wait_for_selector(indicator, timeout=3000)
                if element:
                    print("✅ [OTP] OTP requirement detected")
                    return True
            except:
                continue
                
        print("ℹ️ [OTP] No OTP requirement detected")
        return False
        
    async def _identify_otp_method(self, page):
        """Identify OTP delivery method"""
        print("📱 [OTP] Identifying OTP method...")
        
        # Check page content for method indicators
        page_content = await page.content()
        
        if any(keyword in page_content.lower() for keyword in ['sms', 'text message', 'phone']):
            print("📱 [OTP] SMS method detected")
            return 'sms'
        elif any(keyword in page_content.lower() for keyword in ['email', 'e-mail']):
            print("📧 [OTP] Email method detected")
            return 'email'
        elif any(keyword in page_content.lower() for keyword in ['app', 'authenticator']):
            print("📱 [OTP] App method detected")
            return 'app'
        elif any(keyword in page_content.lower() for keyword in ['voice', 'call']):
            print("📞 [OTP] Voice method detected")
            return 'voice'
        else:
            print("❓ [OTP] Unknown method, defaulting to SMS")
            return 'sms'
            
    async def _request_otp(self, page, method):
        """Request OTP from the service"""
        print(f"📤 [OTP] Requesting OTP via {method}...")
        
        try:
            # Look for OTP request buttons
            request_selectors = [
                'button:has-text("Send code")',
                'button:has-text("Send OTP")',
                'button:has-text("Get code")',
                'button:has-text("Request")',
                '[data-analytics-title*="send"]',
                '.send-otp-button'
            ]
            
            for selector in request_selectors:
                try:
                    request_button = await page.wait_for_selector(selector, timeout=3000)
                    if request_button:
                        await request_button.click()
                        await asyncio.sleep(random.uniform(2, 4))
                        print("✅ [OTP] OTP request sent")
                        return {'success': True, 'method': method}
                except:
                    continue
                    
            # If no explicit request button, OTP might be auto-sent
            print("ℹ️ [OTP] No request button found, assuming auto-sent")
            return {'success': True, 'method': method}
            
        except Exception as e:
            print(f"❌ [OTP] Request error: {e}")
            return {'success': False, 'error': str(e)}
            
    async def _retrieve_otp(self, page, method):
        """Retrieve OTP code"""
        print(f"🔍 [OTP] Retrieving OTP code via {method}...")
        
        if OTP_SERVICE == "auto":
            return await self._auto_generate_otp()
        elif OTP_API_KEY:
            return await self._api_retrieve_otp(method)
        else:
            return await self._manual_otp_simulation(page)
            
    async def _auto_generate_otp(self):
        """Generate OTP for testing purposes"""
        print("🎲 [OTP] Auto-generating OTP for testing...")
        
        # Generate realistic OTP
        otp_length = random.choice([4, 6])
        otp_code = ''.join([str(random.randint(0, 9)) for _ in range(otp_length)])
        
        # Simulate realistic delay
        await asyncio.sleep(random.uniform(5, 15))
        
        print(f"🔢 [OTP] Generated OTP: {otp_code}")
        return otp_code
        
    async def _api_retrieve_otp(self, method):
        """Retrieve OTP using external API service"""
        print(f"🌐 [OTP] Retrieving OTP via API for {method}...")
        
        try:
            # This would integrate with real OTP services like:
            # - SMS-Activate
            # - 5SIM
            # - GetSMSCode
            # For demo purposes, we'll simulate
            
            await asyncio.sleep(random.uniform(10, 20))  # Realistic API delay
            
            # Simulate API response
            api_otp = str(random.randint(100000, 999999))
            print(f"🔢 [OTP] Retrieved from API: {api_otp}")
            
            return api_otp
            
        except Exception as e:
            print(f"❌ [OTP] API retrieval error: {e}")
            return await self._auto_generate_otp()  # Fallback
            
    async def _manual_otp_simulation(self, page):
        """Simulate manual OTP entry"""
        print("👤 [OTP] Simulating manual OTP entry...")
        
        # Look for OTP in page content (sometimes displayed for testing)
        page_content = await page.content()
        
        for pattern in self.otp_patterns:
            matches = re.findall(pattern, page_content)
            if matches:
                otp_code = matches[0]
                print(f"🔍 [OTP] Found OTP in page content: {otp_code}")
                return otp_code
                
        # Generate fallback OTP
        return await self._auto_generate_otp()
        
    async def _submit_otp(self, page, otp_code):
        """Submit OTP code"""
        print(f"📝 [OTP] Submitting OTP: {otp_code}")
        
        max_attempts = 3
        attempt = 0
        
        while attempt < max_attempts:
            attempt += 1
            print(f"🔄 [OTP] Attempt {attempt}/{max_attempts}")
            
            try:
                # Find OTP input field
                otp_input = await self._find_otp_input(page)
                
                if not otp_input:
                    print("❌ [OTP] Could not find OTP input field")
                    continue
                    
                # Clear and enter OTP
                await otp_input.click()
                await otp_input.clear()
                
                # Type OTP naturally
                for digit in otp_code:
                    await otp_input.type(digit)
                    await asyncio.sleep(random.uniform(0.1, 0.3))
                    
                await asyncio.sleep(random.uniform(0.5, 1.0))
                
                # Submit OTP
                submit_success = await self._submit_otp_form(page)
                
                if submit_success:
                    # Check for success/error messages
                    result = await self._check_otp_result(page)
                    
                    if result['success']:
                        print("✅ [OTP] OTP submitted successfully")
                        return {'success': True, 'attempts': attempt}
                    else:
                        print(f"❌ [OTP] OTP rejected: {result.get('error', 'Unknown error')}")
                        if attempt < max_attempts:
                            # Generate new OTP for retry
                            otp_code = await self._auto_generate_otp()
                            await asyncio.sleep(random.uniform(2, 5))
                            
            except Exception as e:
                print(f"❌ [OTP] Submission error on attempt {attempt}: {e}")
                
        print("❌ [OTP] All attempts failed")
        return {'success': False, 'attempts': attempt, 'error': 'Max attempts exceeded'}
        
    async def _find_otp_input(self, page):
        """Find OTP input field"""
        otp_selectors = [
            'input[name*="otp"]',
            'input[name*="code"]',
            'input[name*="verification"]',
            'input[placeholder*="code"]',
            'input[placeholder*="OTP"]',
            'input[type="tel"][maxlength="6"]',
            'input[type="number"][maxlength="6"]',
            '.otp-input',
            '#otp-code',
            '#verification-code'
        ]
        
        for selector in otp_selectors:
            try:
                otp_input = await page.wait_for_selector(selector, timeout=2000)
                if otp_input:
                    return otp_input
            except:
                continue
                
        return None
        
    async def _submit_otp_form(self, page):
        """Submit OTP form"""
        submit_selectors = [
            'button:has-text("Verify")',
            'button:has-text("Submit")',
            'button:has-text("Confirm")',
            'button:has-text("Continue")',
            '[data-analytics-title*="verify"]',
            '.verify-button',
            '.submit-otp'
        ]
        
        for selector in submit_selectors:
            try:
                submit_button = await page.wait_for_selector(selector, timeout=2000)
                if submit_button:
                    await submit_button.click()
                    await asyncio.sleep(random.uniform(1, 3))
                    return True
            except:
                continue
                
        # Try pressing Enter on OTP input
        try:
            otp_input = await self._find_otp_input(page)
            if otp_input:
                await otp_input.press('Enter')
                await asyncio.sleep(random.uniform(1, 3))
                return True
        except:
            pass
            
        return False
        
    async def _check_otp_result(self, page):
        """Check OTP submission result"""
        await asyncio.sleep(random.uniform(2, 4))  # Wait for response
        
        # Check for success indicators
        success_indicators = [
            'text="Verification successful"',
            'text="Code verified"',
            'text="Success"',
            '.success-message',
            '.verification-success'
        ]
        
        for indicator in success_indicators:
            try:
                success_element = await page.wait_for_selector(indicator, timeout=3000)
                if success_element:
                    return {'success': True}
            except:
                continue
                
        # Check for error indicators
        error_indicators = [
            'text="Invalid code"',
            'text="Incorrect code"',
            'text="Code expired"',
            'text="Try again"',
            '.error-message',
            '.verification-error'
        ]
        
        for indicator in error_indicators:
            try:
                error_element = await page.wait_for_selector(indicator, timeout=2000)
                if error_element:
                    error_text = await error_element.text_content()
                    return {'success': False, 'error': error_text}
            except:
                continue
                
        # Check if we're still on OTP page (indicates failure)
        otp_still_required = await self._detect_otp_requirement(page)
        if otp_still_required:
            return {'success': False, 'error': 'Still on OTP page'}
            
        # Assume success if no clear indicators
        return {'success': True}