"""
🛡️ GOD-TIER Browser Stealth Module
Advanced GoLogin integration with maximum anonymity
"""

import os
import random
import asyncio
from playwright.async_api import async_playwright
from fake_useragent import UserAgent
from config import *

try:
    from gologin import GoLogin
    GOLOGIN_AVAILABLE = True
except ImportError:
    GOLOGIN_AVAILABLE = False
    print("⚠️ [WARNING] GoLogin not available, using fallback stealth mode")

class StealthBrowser:
    def __init__(self):
        self.ua = UserAgent()
        self.playwright = None
        self.browser = None
        
    async def setup_stealth_context(self, context):
        """Apply stealth configurations to browser context"""
        
        # Add stealth scripts
        await context.add_init_script("""
            // Override webdriver detection
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
            
            // Override plugins
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
            
            // Override languages
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en', 'th-TH', 'th'],
            });
            
            // Override permissions
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                    Promise.resolve({ state: Notification.permission }) :
                    originalQuery(parameters)
            );
            
            // Override chrome runtime
            window.chrome = {
                runtime: {},
            };
            
            // Override iframe detection
            Object.defineProperty(HTMLIFrameElement.prototype, 'contentWindow', {
                get: function() {
                    return window;
                }
            });
        """)
        
        # Set random viewport
        viewport_width = random.randint(1200, 1920)
        viewport_height = random.randint(800, 1080)
        await context.set_viewport_size({"width": viewport_width, "height": viewport_height})
        
        print(f"🛡️ [STEALTH] Applied stealth configurations - Viewport: {viewport_width}x{viewport_height}")

async def launch_stealth_browser():
    """Launch browser with maximum stealth configuration"""
    
    if GOLOGIN_AVAILABLE and GOLOGIN_API_KEY and GOLOGIN_PROFILE_ID:
        return await launch_gologin_browser()
    else:
        return await launch_fallback_browser()

async def launch_gologin_browser():
    """Launch browser using GoLogin for maximum stealth"""
    try:
        print("🔥 [GOLOGIN] Initializing GoLogin browser...")
        
        gl = GoLogin({
            "token": GOLOGIN_API_KEY,
            "profile_id": GOLOGIN_PROFILE_ID,
        })
        
        debugger_address = gl.start()
        if not debugger_address:
            raise Exception("GoLogin browser failed to start")
            
        print(f"🛡️ [GOLOGIN] Browser started at {debugger_address}")
        
        playwright = await async_playwright().start()
        browser = await playwright.chromium.connect_over_cdp(debugger_address)
        
        # Get existing context or create new one
        contexts = browser.contexts
        if contexts:
            context = contexts[0]
        else:
            context = await browser.new_context()
            
        # Apply additional stealth
        stealth = StealthBrowser()
        await stealth.setup_stealth_context(context)
        
        page = await context.new_page()
        
        # Set additional page configurations
        await page.set_extra_http_headers({
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        })
        
        print("✅ [GOLOGIN] Browser ready with GOD-TIER stealth")
        return browser, context, page
        
    except Exception as e:
        print(f"❌ [GOLOGIN] Failed: {e}")
        print("🔄 [FALLBACK] Switching to fallback browser...")
        return await launch_fallback_browser()

async def launch_fallback_browser():
    """Launch browser with fallback stealth configuration"""
    print("🔄 [FALLBACK] Launching fallback stealth browser...")
    
    playwright = await async_playwright().start()
    
    # Launch with stealth args
    browser = await playwright.chromium.launch(
        headless=BROWSER_HEADLESS,
        args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--disable-gpu',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-features=TranslateUI',
            '--disable-ipc-flooding-protection',
            '--disable-blink-features=AutomationControlled',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor',
            '--user-agent=' + UserAgent().random
        ]
    )
    
    context = await browser.new_context(
        viewport={'width': random.randint(1200, 1920), 'height': random.randint(800, 1080)},
        user_agent=UserAgent().random,
        locale='en-US',
        timezone_id='Asia/Bangkok',
        permissions=['geolocation', 'notifications'],
        geolocation={'latitude': 13.7563, 'longitude': 100.5018},  # Bangkok
        extra_http_headers={
            'Accept-Language': 'en-US,en;q=0.9,th;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
        }
    )
    
    # Apply stealth configurations
    stealth = StealthBrowser()
    await stealth.setup_stealth_context(context)
    
    page = await context.new_page()
    
    print("✅ [FALLBACK] Fallback browser ready with stealth")
    return browser, context, page

async def simulate_human_behavior(page):
    """Simulate human-like behavior on page"""
    
    # Random mouse movements
    for _ in range(random.randint(2, 5)):
        x = random.randint(0, 1200)
        y = random.randint(0, 800)
        await page.mouse.move(x, y)
        await asyncio.sleep(random.uniform(0.1, 0.3))
    
    # Random scrolling
    scroll_amount = random.randint(100, 500)
    await page.evaluate(f"window.scrollBy(0, {scroll_amount});")
    await asyncio.sleep(random.uniform(0.5, 1.5))
    
    # Random wait
    await asyncio.sleep(random.uniform(1, 3))
    
    print("🤖 [HUMAN] Simulated human behavior")