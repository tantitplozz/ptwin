"""
🔥 GOD-TIER Warmup Agent
Advanced human-like browsing patterns for maximum stealth
"""

import random
import asyncio
from datetime import datetime
from .browser_stealth import simulate_human_behavior
from .config import *

# Comprehensive warmup URLs for natural browsing pattern
WARMUP_URLS = [
    # Apple ecosystem
    "https://www.apple.com/th/",
    "https://www.apple.com/th/iphone/",
    "https://www.apple.com/th/iphone-16-pro/",
    "https://www.apple.com/th/mac/",
    "https://www.apple.com/th/ipad/",
    "https://www.apple.com/th/accessories/",
    "https://www.apple.com/th/support/",
    
    # Tech news and reviews
    "https://www.theverge.com/",
    "https://techcrunch.com/",
    "https://www.engadget.com/",
    
    # Shopping comparison
    "https://www.gsmarena.com/",
    "https://www.phonearena.com/",
    
    # Social media (brief visits)
    "https://twitter.com/",
    "https://www.facebook.com/",
    
    # General browsing
    "https://www.google.com/",
    "https://www.youtube.com/",
]

# Search queries for natural behavior
SEARCH_QUERIES = [
    "iPhone 16 Pro Max review",
    "iPhone 16 Pro Max vs iPhone 15 Pro Max",
    "best iPhone 16 Pro Max case",
    "iPhone 16 Pro Max price Thailand",
    "iPhone 16 Pro Max camera test",
    "iPhone 16 Pro Max battery life",
    "iPhone 16 Pro Max colors",
    "iPhone 16 Pro Max storage options",
]

class WarmupAgent:
    def __init__(self, memory_manager):
        self.memory = memory_manager
        self.session_data = {
            'start_time': datetime.now(),
            'visited_urls': [],
            'search_queries': [],
            'interactions': []
        }
    
    async def execute_natural_browsing(self, page):
        """Execute natural browsing pattern"""
        print("🔥 [WARMUP] Starting natural browsing pattern...")
        
        # Phase 1: General browsing
        await self._phase_general_browsing(page)
        
        # Phase 2: Apple ecosystem exploration
        await self._phase_apple_exploration(page)
        
        # Phase 3: Product research
        await self._phase_product_research(page)
        
        # Phase 4: Final preparation
        await self._phase_final_preparation(page)
        
        print("✅ [WARMUP] Natural browsing pattern completed")
        
    async def _phase_general_browsing(self, page):
        """Phase 1: General internet browsing"""
        print("📱 [WARMUP-P1] General browsing phase...")
        
        general_urls = [
            "https://www.google.com/",
            "https://www.youtube.com/",
            "https://www.theverge.com/",
        ]
        
        for url in random.sample(general_urls, k=2):
            await self._visit_url_naturally(page, url)
            await self._perform_search(page, random.choice(SEARCH_QUERIES))
            
    async def _phase_apple_exploration(self, page):
        """Phase 2: Apple ecosystem exploration"""
        print("🍎 [WARMUP-P2] Apple ecosystem exploration...")
        
        apple_urls = [url for url in WARMUP_URLS if "apple.com" in url]
        
        for url in random.sample(apple_urls, k=3):
            await self._visit_url_naturally(page, url)
            await self._explore_page_content(page)
            
    async def _phase_product_research(self, page):
        """Phase 3: Product research and comparison"""
        print("🔍 [WARMUP-P3] Product research phase...")
        
        research_urls = [
            "https://www.gsmarena.com/",
            "https://www.phonearena.com/",
            "https://techcrunch.com/",
        ]
        
        for url in random.sample(research_urls, k=2):
            await self._visit_url_naturally(page, url)
            await self._research_behavior(page)
            
    async def _phase_final_preparation(self, page):
        """Phase 4: Final preparation before purchase"""
        print("🎯 [WARMUP-P4] Final preparation phase...")
        
        # Visit Apple store page
        await self._visit_url_naturally(page, "https://www.apple.com/th/shop/")
        await self._browse_products(page)
        
        # Check iPhone specifically
        await self._visit_url_naturally(page, "https://www.apple.com/th/shop/buy-iphone/")
        await self._compare_models(page)
        
    async def _visit_url_naturally(self, page, url):
        """Visit URL with natural human behavior"""
        try:
            print(f"🌐 [WARMUP] Visiting: {url}")
            
            # Navigate with realistic timing
            await page.goto(url, wait_until='domcontentloaded', timeout=BROWSER_TIMEOUT)
            
            # Wait for page to load naturally
            await asyncio.sleep(random.uniform(2, 5))
            
            # Simulate human behavior
            await simulate_human_behavior(page)
            
            # Record visit
            self.session_data['visited_urls'].append({
                'url': url,
                'timestamp': datetime.now(),
                'duration': random.uniform(10, 30)
            })
            
            self.memory.log("warmup_visit", {
                'url': url,
                'timestamp': datetime.now().isoformat(),
                'phase': 'warmup'
            })
            
        except Exception as e:
            print(f"⚠️ [WARMUP] Error visiting {url}: {e}")
            
    async def _perform_search(self, page, query):
        """Perform search with natural typing"""
        try:
            # Look for search box
            search_selectors = [
                'input[name="q"]',
                'input[type="search"]',
                '#search',
                '.search-input',
                '[placeholder*="search" i]'
            ]
            
            for selector in search_selectors:
                try:
                    search_box = await page.wait_for_selector(selector, timeout=3000)
                    if search_box:
                        # Clear and type naturally
                        await search_box.click()
                        await search_box.clear()
                        
                        # Type with human-like delays
                        for char in query:
                            await search_box.type(char)
                            await asyncio.sleep(random.uniform(0.05, 0.15))
                        
                        # Press Enter
                        await search_box.press('Enter')
                        await asyncio.sleep(random.uniform(2, 4))
                        
                        print(f"🔍 [WARMUP] Searched: {query}")
                        self.session_data['search_queries'].append(query)
                        break
                        
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ [WARMUP] Search error: {e}")
            
    async def _explore_page_content(self, page):
        """Explore page content naturally"""
        try:
            # Scroll through page
            for _ in range(random.randint(2, 4)):
                scroll_amount = random.randint(200, 600)
                await page.evaluate(f"window.scrollBy(0, {scroll_amount});")
                await asyncio.sleep(random.uniform(1, 3))
            
            # Click on random links (but don't navigate)
            links = await page.query_selector_all('a')
            if links:
                random_links = random.sample(links, min(2, len(links)))
                for link in random_links:
                    try:
                        # Hover over link
                        await link.hover()
                        await asyncio.sleep(random.uniform(0.5, 1.5))
                    except:
                        pass
                        
            print("👀 [WARMUP] Explored page content")
            
        except Exception as e:
            print(f"⚠️ [WARMUP] Content exploration error: {e}")
            
    async def _research_behavior(self, page):
        """Simulate research behavior"""
        try:
            # Look for product comparisons or reviews
            comparison_keywords = ['compare', 'review', 'vs', 'best', 'price']
            
            for keyword in random.sample(comparison_keywords, k=2):
                try:
                    # Search for elements containing keyword
                    elements = await page.query_selector_all(f'text="{keyword}"')
                    if elements:
                        element = random.choice(elements)
                        await element.hover()
                        await asyncio.sleep(random.uniform(1, 2))
                except:
                    pass
                    
            # Simulate reading behavior
            await asyncio.sleep(random.uniform(5, 10))
            
            print("📚 [WARMUP] Performed research behavior")
            
        except Exception as e:
            print(f"⚠️ [WARMUP] Research behavior error: {e}")
            
    async def _browse_products(self, page):
        """Browse products naturally"""
        try:
            # Look for product categories
            product_selectors = [
                '[data-analytics-title*="iphone" i]',
                '[href*="iphone"]',
                '.product-tile',
                '.product-card'
            ]
            
            for selector in product_selectors:
                try:
                    products = await page.query_selector_all(selector)
                    if products:
                        # Hover over random products
                        for product in random.sample(products, min(3, len(products))):
                            await product.hover()
                            await asyncio.sleep(random.uniform(1, 2))
                        break
                except:
                    continue
                    
            print("🛍️ [WARMUP] Browsed products")
            
        except Exception as e:
            print(f"⚠️ [WARMUP] Product browsing error: {e}")
            
    async def _compare_models(self, page):
        """Compare iPhone models"""
        try:
            # Look for model comparison elements
            model_selectors = [
                '[data-analytics-title*="pro max" i]',
                '[data-analytics-title*="pro" i]',
                '.compare-button',
                '.model-selector'
            ]
            
            for selector in model_selectors:
                try:
                    elements = await page.query_selector_all(selector)
                    if elements:
                        for element in random.sample(elements, min(2, len(elements))):
                            await element.hover()
                            await asyncio.sleep(random.uniform(1, 3))
                        break
                except:
                    continue
                    
            print("⚖️ [WARMUP] Compared models")
            
        except Exception as e:
            print(f"⚠️ [WARMUP] Model comparison error: {e}")

async def run_warmup(page, memory):
    """Main warmup function"""
    warmup_agent = WarmupAgent(memory)
    
    start_time = datetime.now()
    print(f"🔥 [WARMUP] Starting GOD-TIER warmup at {start_time}")
    
    try:
        await warmup_agent.execute_natural_browsing(page)
        
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        
        # Save warmup session data
        memory.log("warmup_session", {
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'duration': duration,
            'urls_visited': len(warmup_agent.session_data['visited_urls']),
            'searches_performed': len(warmup_agent.session_data['search_queries']),
            'status': 'completed'
        })
        
        print(f"✅ [WARMUP] Completed in {duration:.2f} seconds")
        print(f"📊 [WARMUP] Stats: {len(warmup_agent.session_data['visited_urls'])} URLs, {len(warmup_agent.session_data['search_queries'])} searches")
        
    except Exception as e:
        print(f"❌ [WARMUP] Error: {e}")
        memory.log("warmup_error", {
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        })
        raise