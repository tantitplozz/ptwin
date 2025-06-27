#!/usr/bin/env python3
"""
🧪 GOD-TIER PhantomAutoBuyBot - Test Suite
Comprehensive testing for all modules
"""

import asyncio
import sys
import os
from pathlib import Path

# Add phantom_autobuy to path
sys.path.append(str(Path(__file__).parent / "phantom_autobuy"))

async def test_imports():
    """Test all module imports"""
    print("🧪 [TEST] Testing module imports...")
    
    modules = [
        "config",
        "memory", 
        "browser_stealth",
        "warmup_agent",
        "purchase_flow",
        "payment_patterns",
        "otp",
        "monitor_ws",
        "telegram_notify",
        "ab_tester"
    ]
    
    failed_imports = []
    
    for module in modules:
        try:
            __import__(module)
            print(f"✅ [TEST] {module} imported successfully")
        except ImportError as e:
            print(f"❌ [TEST] {module} import failed: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"❌ [TEST] Failed imports: {', '.join(failed_imports)}")
        return False
    else:
        print("✅ [TEST] All modules imported successfully")
        return True

async def test_configuration():
    """Test configuration loading"""
    print("🧪 [TEST] Testing configuration...")
    
    try:
        import config
        
        # Test required variables
        required_vars = [
            "TARGET_PRODUCT",
            "TARGET_STORAGE", 
            "TARGET_COLOR",
            "MONITOR_PORT",
            "BROWSER_TIMEOUT"
        ]
        
        missing_vars = []
        for var in required_vars:
            if not hasattr(config, var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ [TEST] Missing config variables: {', '.join(missing_vars)}")
            return False
        
        print(f"✅ [TEST] Configuration loaded - Target: {config.TARGET_PRODUCT}")
        return True
        
    except Exception as e:
        print(f"❌ [TEST] Configuration test failed: {e}")
        return False

async def test_memory_system():
    """Test memory system"""
    print("🧪 [TEST] Testing memory system...")
    
    try:
        from memory import MemoryManager
        
        memory = MemoryManager()
        
        # Test logging
        memory.log("test_event", {"test": "data"})
        
        # Test pattern analysis
        patterns = memory.get_success_patterns("test_event")
        
        # Test analytics
        analytics = memory.export_analytics()
        
        print("✅ [TEST] Memory system working correctly")
        return True
        
    except Exception as e:
        print(f"❌ [TEST] Memory system test failed: {e}")
        return False

async def test_telegram_config():
    """Test Telegram configuration"""
    print("🧪 [TEST] Testing Telegram configuration...")
    
    try:
        from telegram_notify import send_telegram
        import config
        
        if not config.TELEGRAM_TOKEN:
            print("⚠️ [TEST] TELEGRAM_TOKEN not configured")
            return False
            
        if not config.TELEGRAM_CHAT_ID:
            print("⚠️ [TEST] TELEGRAM_CHAT_ID not configured")
            return False
            
        print("✅ [TEST] Telegram configuration present")
        
        # Test message sending (dry run)
        print("📱 [TEST] Testing Telegram message (dry run)...")
        # Note: Actual sending would require valid credentials
        
        return True
        
    except Exception as e:
        print(f"❌ [TEST] Telegram test failed: {e}")
        return False

async def test_browser_stealth():
    """Test browser stealth module"""
    print("🧪 [TEST] Testing browser stealth...")
    
    try:
        from browser_stealth import StealthBrowser
        
        stealth = StealthBrowser()
        print("✅ [TEST] StealthBrowser initialized")
        
        # Test user agent generation
        ua = stealth.ua.random
        print(f"✅ [TEST] User agent generated: {ua[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ [TEST] Browser stealth test failed: {e}")
        return False

async def test_ab_testing():
    """Test A/B testing system"""
    print("🧪 [TEST] Testing A/B testing system...")
    
    try:
        from ab_tester import ABTestRunner
        from memory import MemoryManager
        
        memory = MemoryManager()
        ab_tester = ABTestRunner(memory)
        
        # Test profile generation
        profiles = ab_tester.test_profiles
        print(f"✅ [TEST] Generated {len(profiles)} test profiles")
        
        # Test summary
        summary = ab_tester.get_test_summary()
        print(f"✅ [TEST] Test summary generated: {summary['session_id']}")
        
        return True
        
    except Exception as e:
        print(f"❌ [TEST] A/B testing test failed: {e}")
        return False

async def test_monitor_system():
    """Test monitoring system"""
    print("🧪 [TEST] Testing monitor system...")
    
    try:
        from monitor_ws import MonitorServer
        
        monitor = MonitorServer()
        
        # Test status updates
        monitor.update_status("test_key", "test_value")
        
        # Test event logging
        monitor.log_event("test_event", {"test": "data"})
        
        print("✅ [TEST] Monitor system working")
        return True
        
    except Exception as e:
        print(f"❌ [TEST] Monitor system test failed: {e}")
        return False

async def test_payment_system():
    """Test payment system"""
    print("🧪 [TEST] Testing payment system...")
    
    try:
        from payment_patterns import PaymentProcessor
        from memory import MemoryManager
        
        memory = MemoryManager()
        payment = PaymentProcessor(memory)
        
        # Test payment methods
        methods = payment.payment_methods
        print(f"✅ [TEST] Payment methods loaded: {list(methods.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ [TEST] Payment system test failed: {e}")
        return False

async def test_otp_system():
    """Test OTP system"""
    print("🧪 [TEST] Testing OTP system...")
    
    try:
        from otp import OTPHandler
        
        otp_handler = OTPHandler()
        
        # Test OTP patterns
        patterns = otp_handler.otp_patterns
        print(f"✅ [TEST] OTP patterns loaded: {len(patterns)} patterns")
        
        # Test OTP sources
        sources = otp_handler.otp_sources
        print(f"✅ [TEST] OTP sources: {list(sources.keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ [TEST] OTP system test failed: {e}")
        return False

async def run_all_tests():
    """Run all tests"""
    print("🔥 [TEST] Starting GOD-TIER PhantomAutoBuyBot Test Suite")
    print("=" * 60)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_configuration),
        ("Memory System", test_memory_system),
        ("Telegram Config", test_telegram_config),
        ("Browser Stealth", test_browser_stealth),
        ("A/B Testing", test_ab_testing),
        ("Monitor System", test_monitor_system),
        ("Payment System", test_payment_system),
        ("OTP System", test_otp_system)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        print(f"\n🧪 [TEST] Running {test_name}...")
        try:
            result = await test_func()
            if result:
                passed += 1
                print(f"✅ [TEST] {test_name} PASSED")
            else:
                failed += 1
                print(f"❌ [TEST] {test_name} FAILED")
        except Exception as e:
            failed += 1
            print(f"💥 [TEST] {test_name} CRASHED: {e}")
    
    print("\n" + "=" * 60)
    print(f"🧪 [TEST] Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 [TEST] ALL TESTS PASSED! GOD-TIER system ready for deployment!")
        return True
    else:
        print("⚠️ [TEST] Some tests failed. Please fix issues before deployment.")
        return False

async def main():
    """Main test function"""
    success = await run_all_tests()
    
    if success:
        print("\n🚀 [TEST] System ready for deployment!")
        print("💡 [TEST] Next steps:")
        print("   1. Configure .env file with your credentials")
        print("   2. Run: python run.py")
        print("   3. Choose deployment option")
        print("   4. Monitor at http://localhost:8686")
    else:
        print("\n🔧 [TEST] Please fix the issues above before proceeding.")
        
    return success

if __name__ == "__main__":
    result = asyncio.run(main())
    sys.exit(0 if result else 1)