"""
📱 GOD-TIER Telegram Notification System
Advanced real-time notifications with rich formatting
"""

import asyncio
import aiohttp
import json
from datetime import datetime
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

class TelegramNotifier:
    def __init__(self):
        self.base_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
        self.session = None
        self.message_queue = []
        self.is_sending = False
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    async def send_message(self, text, parse_mode='HTML', disable_notification=False):
        """Send message to Telegram"""
        if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
            print(f"📱 [TELEGRAM] Not configured - would send: {text}")
            return False
            
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
                
            url = f"{self.base_url}/sendMessage"
            data = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': text,
                'parse_mode': parse_mode,
                'disable_notification': disable_notification
            }
            
            async with self.session.post(url, data=data) as response:
                if response.status == 200:
                    print(f"✅ [TELEGRAM] Message sent successfully")
                    return True
                else:
                    error_text = await response.text()
                    print(f"❌ [TELEGRAM] Send failed: {response.status} - {error_text}")
                    return False
                    
        except Exception as e:
            print(f"❌ [TELEGRAM] Error: {e}")
            return False
            
    async def send_photo(self, photo_path, caption=None):
        """Send photo to Telegram"""
        if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
            print(f"📱 [TELEGRAM] Not configured - would send photo: {photo_path}")
            return False
            
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
                
            url = f"{self.base_url}/sendPhoto"
            
            with open(photo_path, 'rb') as photo:
                data = aiohttp.FormData()
                data.add_field('chat_id', TELEGRAM_CHAT_ID)
                data.add_field('photo', photo, filename='screenshot.png')
                if caption:
                    data.add_field('caption', caption)
                    
                async with self.session.post(url, data=data) as response:
                    if response.status == 200:
                        print(f"✅ [TELEGRAM] Photo sent successfully")
                        return True
                    else:
                        error_text = await response.text()
                        print(f"❌ [TELEGRAM] Photo send failed: {response.status} - {error_text}")
                        return False
                        
        except Exception as e:
            print(f"❌ [TELEGRAM] Photo error: {e}")
            return False
            
    async def send_document(self, document_path, caption=None):
        """Send document to Telegram"""
        if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
            print(f"📱 [TELEGRAM] Not configured - would send document: {document_path}")
            return False
            
        try:
            if not self.session:
                self.session = aiohttp.ClientSession()
                
            url = f"{self.base_url}/sendDocument"
            
            with open(document_path, 'rb') as document:
                data = aiohttp.FormData()
                data.add_field('chat_id', TELEGRAM_CHAT_ID)
                data.add_field('document', document, filename=document_path.split('/')[-1])
                if caption:
                    data.add_field('caption', caption)
                    
                async with self.session.post(url, data=data) as response:
                    if response.status == 200:
                        print(f"✅ [TELEGRAM] Document sent successfully")
                        return True
                    else:
                        error_text = await response.text()
                        print(f"❌ [TELEGRAM] Document send failed: {response.status} - {error_text}")
                        return False
                        
        except Exception as e:
            print(f"❌ [TELEGRAM] Document error: {e}")
            return False

# Global notifier instance
notifier = TelegramNotifier()

async def send_telegram(message, parse_mode='HTML', disable_notification=False):
    """Send simple telegram message"""
    return await notifier.send_message(message, parse_mode, disable_notification)

async def send_startup_notification():
    """Send bot startup notification"""
    message = """
🔥 <b>GOD-TIER PhantomAutoBuyBot STARTED</b> 🔥

🤖 <b>Status:</b> Initializing
⏰ <b>Time:</b> {timestamp}
🎯 <b>Target:</b> iPhone 16 Pro Max
💾 <b>Storage:</b> 1TB
🎨 <b>Color:</b> Natural Titanium

🛡️ <b>Stealth Mode:</b> ACTIVATED
🧠 <b>AI Memory:</b> LOADED
📊 <b>Monitor:</b> ws://localhost:8686

<i>All systems ready for GOD-TIER operation!</i>
    """.format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    
    return await send_telegram(message)

async def send_warmup_notification(stats):
    """Send warmup completion notification"""
    message = f"""
🔥 <b>WARMUP PHASE COMPLETED</b> ✅

📊 <b>Statistics:</b>
• URLs Visited: {stats.get('urls_visited', 0)}
• Searches Performed: {stats.get('searches_performed', 0)}
• Duration: {stats.get('duration', 0):.1f}s

🛡️ <b>Stealth Status:</b> OPTIMAL
🧠 <b>Behavioral Pattern:</b> HUMAN-LIKE
🎯 <b>Next Phase:</b> Product Selection

<i>Ready for purchase execution!</i>
    """
    
    return await send_telegram(message)

async def send_purchase_start_notification():
    """Send purchase start notification"""
    message = """
🛒 <b>PURCHASE FLOW INITIATED</b> 🚀

📱 <b>Target Product:</b> iPhone 16 Pro Max
💾 <b>Storage:</b> 1TB
🎨 <b>Color:</b> Natural Titanium
📦 <b>Carrier:</b> Unlocked

⚡ <b>Status:</b> Navigating to product page
🛡️ <b>Stealth:</b> MAXIMUM
🤖 <b>AI Mode:</b> GOD-TIER

<i>Executing purchase with precision...</i>
    """
    
    return await send_telegram(message)

async def send_step_notification(step, total_steps, action, status="in_progress"):
    """Send step progress notification"""
    progress_bar = "█" * (step * 10 // total_steps) + "░" * (10 - (step * 10 // total_steps))
    
    status_emoji = {
        "in_progress": "⚡",
        "completed": "✅",
        "failed": "❌",
        "warning": "⚠️"
    }
    
    message = f"""
{status_emoji.get(status, "⚡")} <b>STEP {step}/{total_steps}</b>

🎯 <b>Action:</b> {action}
📊 <b>Progress:</b> [{progress_bar}] {(step * 100 // total_steps)}%
⏰ <b>Time:</b> {datetime.now().strftime("%H:%M:%S")}

<i>GOD-TIER execution in progress...</i>
    """
    
    return await send_telegram(message, disable_notification=True)

async def send_payment_notification(method, status, details=None):
    """Send payment processing notification"""
    status_emoji = {
        "processing": "💳",
        "success": "✅",
        "failed": "❌",
        "pending": "⏳"
    }
    
    message = f"""
{status_emoji.get(status, "💳")} <b>PAYMENT {status.upper()}</b>

💳 <b>Method:</b> {method.replace('_', ' ').title()}
📊 <b>Status:</b> {status.title()}
⏰ <b>Time:</b> {datetime.now().strftime("%H:%M:%S")}
    """
    
    if details:
        message += f"\n📝 <b>Details:</b> {details}"
        
    message += "\n\n<i>Processing with GOD-TIER security...</i>"
    
    return await send_telegram(message)

async def send_otp_notification(otp_code, method, status):
    """Send OTP notification"""
    status_emoji = {
        "received": "📱",
        "submitted": "✅",
        "failed": "❌",
        "pending": "⏳"
    }
    
    message = f"""
{status_emoji.get(status, "📱")} <b>OTP {status.upper()}</b>

🔐 <b>Code:</b> <code>{otp_code}</code>
📱 <b>Method:</b> {method.upper()}
⏰ <b>Time:</b> {datetime.now().strftime("%H:%M:%S")}

<i>GOD-TIER OTP handling activated!</i>
    """
    
    return await send_telegram(message)

async def send_success_notification(order_id, duration, details=None):
    """Send successful purchase notification"""
    message = f"""
🎉 <b>MISSION ACCOMPLISHED!</b> 🎉

✅ <b>Purchase Status:</b> SUCCESS
📱 <b>Product:</b> iPhone 16 Pro Max 1TB
🎨 <b>Color:</b> Natural Titanium
📦 <b>Order ID:</b> <code>{order_id}</code>

⏱️ <b>Total Time:</b> {duration:.1f} seconds
🛡️ <b>Stealth Status:</b> UNDETECTED
🤖 <b>AI Performance:</b> FLAWLESS

🔥 <b>GOD-TIER OPERATION COMPLETE!</b> 🔥

<i>Another successful mission by PhantomAutoBuyBot!</i>
    """
    
    return await send_telegram(message)

async def send_error_notification(error, step=None, context=None):
    """Send error notification"""
    message = f"""
❌ <b>ERROR DETECTED</b> ⚠️

🚨 <b>Error:</b> {str(error)[:200]}
    """
    
    if step:
        message += f"\n📍 <b>Step:</b> {step}"
        
    if context:
        message += f"\n📝 <b>Context:</b> {context}"
        
    message += f"""
⏰ <b>Time:</b> {datetime.now().strftime("%H:%M:%S")}

🔄 <b>Status:</b> Attempting recovery...
🛡️ <b>Stealth:</b> Maintained

<i>GOD-TIER error handling activated!</i>
    """
    
    return await send_telegram(message)

async def send_detection_warning(detection_type, risk_level, recommendations):
    """Send detection warning"""
    risk_emoji = {
        "LOW": "🟢",
        "MEDIUM": "🟡", 
        "HIGH": "🔴"
    }
    
    message = f"""
🛡️ <b>DETECTION ALERT</b> {risk_emoji.get(risk_level, "⚠️")}

🚨 <b>Type:</b> {detection_type}
📊 <b>Risk Level:</b> {risk_level}
⏰ <b>Time:</b> {datetime.now().strftime("%H:%M:%S")}

🔧 <b>Recommendations:</b>
    """
    
    for i, rec in enumerate(recommendations[:3], 1):
        message += f"\n{i}. {rec}"
        
    message += "\n\n<i>Adjusting stealth parameters...</i>"
    
    return await send_telegram(message)

async def send_ab_test_notification(results):
    """Send A/B test results notification"""
    message = """
🧪 <b>A/B TEST COMPLETED</b> 📊

🎯 <b>Test Results:</b>
    """
    
    for i, result in enumerate(results[:3], 1):
        status_emoji = "✅" if result.get('status') == 'success' else "❌"
        message += f"\n{status_emoji} Profile {i}: {result.get('status', 'unknown')}"
        
    best_profile = max(results, key=lambda x: x.get('success_score', 0))
    message += f"""

🏆 <b>Best Profile:</b> {best_profile.get('name', 'Unknown')}
📈 <b>Success Rate:</b> {best_profile.get('success_score', 0):.1%}

<i>Proceeding with optimal configuration!</i>
    """
    
    return await send_telegram(message)

async def send_screenshot_notification(screenshot_path, caption=None):
    """Send screenshot notification"""
    if not caption:
        caption = f"📸 GOD-TIER Screenshot - {datetime.now().strftime('%H:%M:%S')}"
        
    return await notifier.send_photo(screenshot_path, caption)

async def send_shutdown_notification(reason="Manual stop"):
    """Send bot shutdown notification"""
    message = f"""
🛑 <b>GOD-TIER PhantomAutoBuyBot STOPPED</b>

📊 <b>Reason:</b> {reason}
⏰ <b>Time:</b> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

🧹 <b>Status:</b> All resources cleaned up
💾 <b>Memory:</b> Session data saved
🛡️ <b>Security:</b> All traces cleared

<i>Until next mission... 🔥</i>
    """
    
    return await send_telegram(message)

# Batch notification functions
async def send_batch_notifications(notifications):
    """Send multiple notifications efficiently"""
    tasks = []
    for notification in notifications:
        if isinstance(notification, dict):
            task = send_telegram(
                notification.get('message', ''),
                notification.get('parse_mode', 'HTML'),
                notification.get('disable_notification', False)
            )
            tasks.append(task)
        else:
            tasks.append(send_telegram(str(notification)))
            
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

# Queue management for rate limiting
class NotificationQueue:
    def __init__(self, max_per_minute=20):
        self.queue = []
        self.max_per_minute = max_per_minute
        self.sent_times = []
        
    async def add_notification(self, message, priority=1):
        """Add notification to queue with priority"""
        self.queue.append({
            'message': message,
            'priority': priority,
            'timestamp': datetime.now()
        })
        
        # Sort by priority
        self.queue.sort(key=lambda x: x['priority'], reverse=True)
        
        # Process queue
        await self._process_queue()
        
    async def _process_queue(self):
        """Process notification queue with rate limiting"""
        now = datetime.now()
        
        # Remove old timestamps
        self.sent_times = [t for t in self.sent_times if (now - t).seconds < 60]
        
        # Check rate limit
        if len(self.sent_times) >= self.max_per_minute:
            return
            
        # Send notifications
        while self.queue and len(self.sent_times) < self.max_per_minute:
            notification = self.queue.pop(0)
            success = await send_telegram(notification['message'])
            
            if success:
                self.sent_times.append(now)
                
# Global notification queue
notification_queue = NotificationQueue()