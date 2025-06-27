#!/usr/bin/env python3
"""
🔥 GOD-TIER PhantomAutoBuyBot - Health Check System
Verifies all components are properly configured and working
"""

import os
import sys
import asyncio
import aiohttp
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class HealthChecker:
    def __init__(self):
        self.checks = []
        self.passed = 0
        self.failed = 0
        
    def add_check(self, name, status, message=""):
        """Add a health check result"""
        self.checks.append({
            'name': name,
            'status': status,
            'message': message
        })
        
        if status:
            self.passed += 1
        else:
            self.failed += 1
            
    def print_results(self):
        """Print all health check results"""
        print("🔥 GOD-TIER PhantomAutoBuyBot - Health Check")
        print("=" * 50)
        
        for check in self.checks:
            status_icon = "✅" if check['status'] else "❌"
            print(f"{status_icon} {check['name']}")
            if check['message']:
                print(f"   {check['message']}")
        
        print("=" * 50)
        print(f"📊 Results: {self.passed} passed, {self.failed} failed")
        
        if self.failed == 0:
            print("🎉 All checks passed! System is ready!")
            return True
        else:
            print("⚠️ Some checks failed. Please review configuration.")
            return False

async def check_python_version():
    """Check Python version"""
    version = sys.version_info
    required = (3, 11)
    
    if version >= required:
        return True, f"Python {version.major}.{version.minor}.{version.micro}"
    else:
        return False, f"Python {version.major}.{version.minor} (requires 3.11+)"

async def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'playwright',
        'aiohttp',
        'python-dotenv',
        'fake-useragent'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if not missing:
        return True, f"All {len(required_packages)} packages installed"
    else:
        return False, f"Missing packages: {', '.join(missing)}"

async def check_environment_variables():
    """Check if required environment variables are set"""
    required_vars = [
        'GOLOGIN_API_KEY',
        'TELEGRAM_TOKEN',
        'TELEGRAM_CHAT_ID'
    ]
    
    missing = []
    placeholder_values = ['your_', 'your-', 'placeholder', 'example']
    
    for var in required_vars:
        value = os.getenv(var)
        if not value:
            missing.append(f"{var} (not set)")
        elif any(placeholder in value.lower() for placeholder in placeholder_values):
            missing.append(f"{var} (placeholder value)")
    
    if not missing:
        return True, "All required variables configured"
    else:
        return False, f"Issues: {', '.join(missing)}"

async def check_gologin_api():
    """Check GoLogin API connectivity"""
    api_key = os.getenv('GOLOGIN_API_KEY')
    if not api_key or 'your_' in api_key:
        return False, "API key not configured"
    
    try:
        async with aiohttp.ClientSession() as session:
            headers = {'Authorization': f'Bearer {api_key}'}
            async with session.get('https://api.gologin.com/browser', headers=headers, timeout=10) as response:
                if response.status == 200:
                    return True, "API connection successful"
                else:
                    return False, f"API error: {response.status}"
    except Exception as e:
        return False, f"Connection failed: {str(e)}"

async def check_telegram_bot():
    """Check Telegram bot connectivity"""
    token = os.getenv('TELEGRAM_TOKEN')
    if not token or 'your_' in token:
        return False, "Bot token not configured"
    
    try:
        async with aiohttp.ClientSession() as session:
            url = f"https://api.telegram.org/bot{token}/getMe"
            async with session.get(url, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('ok'):
                        bot_info = data['result']
                        return True, f"Bot @{bot_info.get('username', 'unknown')} connected"
                    else:
                        return False, f"Bot error: {data.get('description', 'unknown')}"
                else:
                    return False, f"HTTP error: {response.status}"
    except Exception as e:
        return False, f"Connection failed: {str(e)}"

async def check_file_structure():
    """Check if required files and directories exist"""
    required_files = [
        'phantom_autobuy/main.py',
        'phantom_autobuy/purchase_flow.py',
        'phantom_autobuy/ab_tester.py',
        'requirements.txt',
        '.env.template'
    ]
    
    required_dirs = [
        'phantom_autobuy',
        'logs',
        'screenshots',
        'data'
    ]
    
    missing_files = [f for f in required_files if not Path(f).exists()]
    missing_dirs = [d for d in required_dirs if not Path(d).exists()]
    
    if not missing_files and not missing_dirs:
        return True, "All files and directories present"
    else:
        missing = []
        if missing_files:
            missing.append(f"files: {', '.join(missing_files)}")
        if missing_dirs:
            missing.append(f"dirs: {', '.join(missing_dirs)}")
        return False, f"Missing {'; '.join(missing)}"

async def check_playwright_browsers():
    """Check if Playwright browsers are installed"""
    try:
        from playwright.async_api import async_playwright
        
        async with async_playwright() as p:
            try:
                browser = await p.chromium.launch(headless=True)
                await browser.close()
                return True, "Chromium browser available"
            except Exception as e:
                return False, f"Browser launch failed: {str(e)}"
    except ImportError:
        return False, "Playwright not installed"
    except Exception as e:
        return False, f"Browser check failed: {str(e)}"

async def check_memory_system():
    """Check memory system functionality"""
    try:
        from phantom_autobuy.memory import VectorMemory
        
        # Test memory initialization
        memory = VectorMemory()
        
        # Test basic operations
        memory.add_event('test', {'test': True})
        
        # Test save/load
        await memory.save()
        
        return True, "Memory system functional"
    except Exception as e:
        return False, f"Memory system error: {str(e)}"

async def check_monitoring_system():
    """Check WebSocket monitoring system"""
    try:
        from phantom_autobuy.monitor_ws import start_monitor_server
        
        # Just check if the module can be imported and function exists
        if callable(start_monitor_server):
            return True, "Monitoring system available"
        else:
            return False, "Monitoring function not callable"
    except Exception as e:
        return False, f"Monitoring system error: {str(e)}"

async def main():
    """Run all health checks"""
    checker = HealthChecker()
    
    # Run all checks
    checks = [
        ("Python Version", check_python_version()),
        ("Dependencies", check_dependencies()),
        ("Environment Variables", check_environment_variables()),
        ("File Structure", check_file_structure()),
        ("Playwright Browsers", check_playwright_browsers()),
        ("Memory System", check_memory_system()),
        ("Monitoring System", check_monitoring_system()),
        ("GoLogin API", check_gologin_api()),
        ("Telegram Bot", check_telegram_bot()),
    ]
    
    for name, check_coro in checks:
        try:
            status, message = await check_coro
            checker.add_check(name, status, message)
        except Exception as e:
            checker.add_check(name, False, f"Check failed: {str(e)}")
    
    # Print results
    success = checker.print_results()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    asyncio.run(main())