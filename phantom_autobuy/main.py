#!/usr/bin/env python3
"""
🔥 GOD-TIER PhantomAutoBuyBot - Main Entry Point
Full Stack: Warmup + Memory + Stealth + Payment + OTP + Monitor + Telegram + A/B
"""

import asyncio
import sys
import traceback
from datetime import datetime

from browser_stealth import launch_stealth_browser
from warmup_agent import run_warmup
from purchase_flow import buy_iphone
from memory import MemoryManager
from ab_tester import ABTestRunner
from monitor_ws import start_monitor
from telegram_notify import send_telegram
from config import *

class PhantomAutoBuyBot:
    def __init__(self):
        self.memory = MemoryManager()
        self.ab_tester = ABTestRunner(self.memory)
        self.browser = None
        self.context = None
        self.page = None
        self.monitor_task = None
        
    async def initialize(self):
        """Initialize all components"""
        print("🔥 [GOD-TIER] Initializing PhantomAutoBuyBot...")
        
        # Start WebSocket Monitor
        self.monitor_task = asyncio.create_task(start_monitor())
        print(f"📊 [MONITOR] WebSocket server starting on {MONITOR_HOST}:{MONITOR_PORT}")
        
        # Initialize browser
        self.browser, self.context, self.page = await launch_stealth_browser()
        print("🛡️ [STEALTH] Browser initialized with GoLogin")
        
        # Send startup notification
        await send_telegram("🔥 GOD-TIER PhantomAutoBuyBot STARTED! 🤖")
        
    async def run_full_flow(self):
        """Execute complete GOD-TIER flow"""
        try:
            start_time = datetime.now()
            print(f"🚀 [FLOW] Starting full GOD-TIER flow at {start_time}")
            
            # Phase 1: Warmup Agent
            print("🔥 [PHASE 1] Running Warmup Agent...")
            await run_warmup(self.page, self.memory)
            await send_telegram("✅ Phase 1: Warmup completed")
            
            # Phase 2: A/B Testing with Multiple Profiles
            print("🔥 [PHASE 2] Running A/B Testing...")
            result = await self.ab_tester.run_flows(self.page, buy_iphone)
            await send_telegram(f"✅ Phase 2: A/B Testing completed - Best result: {result['status']}")
            
            # Phase 3: Final execution with best profile
            print("🔥 [PHASE 3] Final execution...")
            final_result = await buy_iphone(self.page, self.memory, result.get('best_profile'))
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # Success notification
            success_msg = f"""
🎉 GOD-TIER MISSION COMPLETED! 🎉

⏱️ Duration: {duration:.2f} seconds
📱 Product: {TARGET_PRODUCT}
💾 Storage: {TARGET_STORAGE}
🎨 Color: {TARGET_COLOR}
📊 Status: {final_result['status']}
🔐 OTP: {final_result.get('otp', 'N/A')}

🤖 All systems performed flawlessly!
            """
            
            await send_telegram(success_msg)
            print("🎉 [SUCCESS] GOD-TIER mission completed!")
            
            return final_result
            
        except Exception as e:
            error_msg = f"❌ GOD-TIER ERROR: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
            await send_telegram(error_msg)
            print(f"❌ [ERROR] {error_msg}")
            raise
            
    async def cleanup(self):
        """Cleanup resources"""
        print("🧹 [CLEANUP] Cleaning up resources...")
        
        if self.page:
            await self.page.screenshot(path="final_screenshot.png")
            
        if self.context:
            await self.context.close()
            
        if self.browser:
            await self.browser.close()
            
        if self.monitor_task:
            self.monitor_task.cancel()
            
        await self.memory.save()
        await send_telegram("🛑 GOD-TIER PhantomAutoBuyBot STOPPED")
        print("✅ [CLEANUP] All resources cleaned up")

async def main():
    """Main execution function"""
    bot = PhantomAutoBuyBot()
    
    try:
        await bot.initialize()
        result = await bot.run_full_flow()
        print(f"🎯 [FINAL] Mission result: {result}")
        
    except KeyboardInterrupt:
        print("⚠️ [INTERRUPT] Received keyboard interrupt")
        await send_telegram("⚠️ GOD-TIER Bot interrupted by user")
        
    except Exception as e:
        print(f"💥 [FATAL] Fatal error: {e}")
        await send_telegram(f"💥 FATAL ERROR: {e}")
        sys.exit(1)
        
    finally:
        await bot.cleanup()

if __name__ == "__main__":
    print("🔥 GOD-TIER PhantomAutoBuyBot Starting...")
    print("=" * 50)
    asyncio.run(main())