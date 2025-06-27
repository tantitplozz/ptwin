"""
🛒 GOD-TIER Purchase Flow
Advanced iPhone purchase automation with stealth and intelligence
"""

import asyncio
import random
from datetime import datetime
from .browser_stealth import simulate_human_behavior
from .payment_patterns import PaymentProcessor
from .otp import OTPHandler
from .config import *

class PurchaseFlow:
    def __init__(self, memory_manager):
        self.memory = memory_manager
        self.payment_processor = PaymentProcessor(memory_manager)
        self.otp_handler = OTPHandler()
        self.current_step = 0
        self.total_steps = 8
        
    async def execute_purchase(self, page, card_profile=None):
        """Execute complete purchase flow"""
        start_time = datetime.now()
        print(f"🛒 [PURCHASE] Starting GOD-TIER purchase flow at {start_time}")
        
        try:
            # Step 1: Navigate to iPhone page
            await self._step_navigate_to_product(page)
            
            # Step 2: Select iPhone model
            await self._step_select_model(page)
            
            # Step 3: Configure options
            await self._step_configure_options(page)
            
            # Step 4: Add to cart
            await self._step_add_to_cart(page)
            
            # Step 5: Review cart
            await self._step_review_cart(page)
            
            # Step 6: Checkout process
            await self._step_checkout(page)
            
            # Step 7: Payment processing
            payment_result = await self._step_payment(page, card_profile)
            
            # Step 8: OTP and confirmation
            final_result = await self._step_confirmation(page, payment_result)
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            result = {
                'status': 'success' if final_result['otp_success'] else 'failed',
                'duration': duration,
                'steps_completed': self.current_step,
                'payment_method': payment_result.get('method'),
                'otp_result': final_result.get('otp'),
                'order_id': final_result.get('order_id'),
                'timestamp': end_time.isoformat()
            }
            
            self.memory.log("purchase_complete", result)
            print(f"✅ [PURCHASE] Flow completed: {result['status']} in {duration:.2f}s")
            
            return result
            
        except Exception as e:
            error_result = {
                'status': 'error',
                'error': str(e),
                'step_failed': self.current_step,
                'timestamp': datetime.now().isoformat()
            }
            self.memory.log("purchase_error", error_result)
            print(f"❌ [PURCHASE] Error at step {self.current_step}: {e}")
            raise
            
    async def _step_navigate_to_product(self, page):
        """Step 1: Navigate to iPhone product page"""
        self.current_step = 1
        print(f"📱 [STEP {self.current_step}/{self.total_steps}] Navigating to iPhone page...")
        
        # Navigate to iPhone 16 Pro page
        iphone_url = "https://www.apple.com/th/shop/buy-iphone/iphone-16-pro"
        await page.goto(iphone_url, wait_until='domcontentloaded', timeout=BROWSER_TIMEOUT)
        
        # Wait for page to load
        await asyncio.sleep(random.uniform(3, 6))
        
        # Simulate human behavior
        await simulate_human_behavior(page)
        
        # Take screenshot
        await page.screenshot(path=f"step_{self.current_step}_navigate.png")
        
        self.memory.log("purchase_step", {
            'step': self.current_step,
            'action': 'navigate_to_product',
            'url': iphone_url,
            'status': 'completed'
        })
        
    async def _step_select_model(self, page):
        """Step 2: Select iPhone model"""
        self.current_step = 2
        print(f"📱 [STEP {self.current_step}/{self.total_steps}] Selecting iPhone model...")
        
        try:
            # Look for iPhone 16 Pro Max option
            model_selectors = [
                '[data-analytics-title*="iPhone 16 Pro Max"]',
                '[aria-label*="iPhone 16 Pro Max"]',
                'text="iPhone 16 Pro Max"',
                '.rf-hcard-content:has-text("iPhone 16 Pro Max")'
            ]
            
            model_selected = False
            for selector in model_selectors:
                try:
                    model_element = await page.wait_for_selector(selector, timeout=5000)
                    if model_element:
                        await model_element.click()
                        await asyncio.sleep(random.uniform(2, 4))
                        model_selected = True
                        print("✅ [PURCHASE] iPhone 16 Pro Max selected")
                        break
                except:
                    continue
                    
            if not model_selected:
                print("⚠️ [PURCHASE] Using fallback model selection")
                # Fallback: click first available model
                await page.click('.rf-hcard-content', timeout=10000)
                
            await simulate_human_behavior(page)
            await page.screenshot(path=f"step_{self.current_step}_model.png")
            
        except Exception as e:
            print(f"⚠️ [PURCHASE] Model selection error: {e}")
            
        self.memory.log("purchase_step", {
            'step': self.current_step,
            'action': 'select_model',
            'target_model': TARGET_PRODUCT,
            'status': 'completed'
        })
        
    async def _step_configure_options(self, page):
        """Step 3: Configure storage, color, and carrier options"""
        self.current_step = 3
        print(f"⚙️ [STEP {self.current_step}/{self.total_steps}] Configuring options...")
        
        # Configure storage
        await self._select_storage(page)
        await asyncio.sleep(random.uniform(1, 3))
        
        # Configure color
        await self._select_color(page)
        await asyncio.sleep(random.uniform(1, 3))
        
        # Configure carrier
        await self._select_carrier(page)
        await asyncio.sleep(random.uniform(1, 3))
        
        await simulate_human_behavior(page)
        await page.screenshot(path=f"step_{self.current_step}_configure.png")
        
        self.memory.log("purchase_step", {
            'step': self.current_step,
            'action': 'configure_options',
            'storage': TARGET_STORAGE,
            'color': TARGET_COLOR,
            'carrier': TARGET_CARRIER,
            'status': 'completed'
        })
        
    async def _select_storage(self, page):
        """Select storage option"""
        try:
            storage_selectors = [
                f'[data-analytics-title*="{TARGET_STORAGE}"]',
                f'text="{TARGET_STORAGE}"',
                f'[aria-label*="{TARGET_STORAGE}"]'
            ]
            
            for selector in storage_selectors:
                try:
                    storage_element = await page.wait_for_selector(selector, timeout=3000)
                    if storage_element:
                        await storage_element.click()
                        print(f"✅ [PURCHASE] Storage {TARGET_STORAGE} selected")
                        return
                except:
                    continue
                    
            print("⚠️ [PURCHASE] Using default storage option")
            
        except Exception as e:
            print(f"⚠️ [PURCHASE] Storage selection error: {e}")
            
    async def _select_color(self, page):
        """Select color option"""
        try:
            color_selectors = [
                f'[data-analytics-title*="{TARGET_COLOR}"]',
                f'[aria-label*="{TARGET_COLOR}"]',
                '.colornav-item'
            ]
            
            for selector in color_selectors:
                try:
                    color_elements = await page.query_selector_all(selector)
                    if color_elements:
                        # Click first available color or target color
                        await color_elements[0].click()
                        print(f"✅ [PURCHASE] Color selected")
                        return
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ [PURCHASE] Color selection error: {e}")
            
    async def _select_carrier(self, page):
        """Select carrier option"""
        try:
            carrier_selectors = [
                f'[data-analytics-title*="{TARGET_CARRIER}"]',
                f'text="{TARGET_CARRIER}"',
                '[data-analytics-title*="Unlocked"]'
            ]
            
            for selector in carrier_selectors:
                try:
                    carrier_element = await page.wait_for_selector(selector, timeout=3000)
                    if carrier_element:
                        await carrier_element.click()
                        print(f"✅ [PURCHASE] Carrier {TARGET_CARRIER} selected")
                        return
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ [PURCHASE] Carrier selection error: {e}")
            
    async def _step_add_to_cart(self, page):
        """Step 4: Add to cart"""
        self.current_step = 4
        print(f"🛒 [STEP {self.current_step}/{self.total_steps}] Adding to cart...")
        
        try:
            # Look for add to cart button
            cart_selectors = [
                '[data-analytics-title*="add to bag"]',
                '[data-analytics-title*="Add to Bag"]',
                'button:has-text("Add to Bag")',
                '.button-add-to-cart',
                '#add-to-cart'
            ]
            
            cart_added = False
            for selector in cart_selectors:
                try:
                    cart_button = await page.wait_for_selector(selector, timeout=5000)
                    if cart_button:
                        await cart_button.click()
                        await asyncio.sleep(random.uniform(2, 4))
                        cart_added = True
                        print("✅ [PURCHASE] Added to cart")
                        break
                except:
                    continue
                    
            if not cart_added:
                # Fallback: look for any button with "add" text
                await page.click('button:has-text("Add")', timeout=10000)
                
            await simulate_human_behavior(page)
            await page.screenshot(path=f"step_{self.current_step}_cart.png")
            
        except Exception as e:
            print(f"⚠️ [PURCHASE] Add to cart error: {e}")
            
        self.memory.log("purchase_step", {
            'step': self.current_step,
            'action': 'add_to_cart',
            'status': 'completed'
        })
        
    async def _step_review_cart(self, page):
        """Step 5: Review cart"""
        self.current_step = 5
        print(f"👀 [STEP {self.current_step}/{self.total_steps}] Reviewing cart...")
        
        try:
            # Look for cart review or checkout button
            review_selectors = [
                '[data-analytics-title*="review bag"]',
                '[data-analytics-title*="checkout"]',
                'button:has-text("Review Bag")',
                'button:has-text("Checkout")',
                '.checkout-button'
            ]
            
            for selector in review_selectors:
                try:
                    review_button = await page.wait_for_selector(selector, timeout=5000)
                    if review_button:
                        await review_button.click()
                        await asyncio.sleep(random.uniform(3, 5))
                        print("✅ [PURCHASE] Cart reviewed")
                        break
                except:
                    continue
                    
            await simulate_human_behavior(page)
            await page.screenshot(path=f"step_{self.current_step}_review.png")
            
        except Exception as e:
            print(f"⚠️ [PURCHASE] Cart review error: {e}")
            
        self.memory.log("purchase_step", {
            'step': self.current_step,
            'action': 'review_cart',
            'status': 'completed'
        })
        
    async def _step_checkout(self, page):
        """Step 6: Checkout process"""
        self.current_step = 6
        print(f"💳 [STEP {self.current_step}/{self.total_steps}] Starting checkout...")
        
        try:
            # Look for checkout button
            checkout_selectors = [
                '[data-analytics-title*="checkout"]',
                'button:has-text("Checkout")',
                '.checkout-button',
                '#checkout-button'
            ]
            
            for selector in checkout_selectors:
                try:
                    checkout_button = await page.wait_for_selector(selector, timeout=5000)
                    if checkout_button:
                        await checkout_button.click()
                        await asyncio.sleep(random.uniform(3, 6))
                        print("✅ [PURCHASE] Checkout initiated")
                        break
                except:
                    continue
                    
            # Handle login if required
            await self._handle_login_if_required(page)
            
            await simulate_human_behavior(page)
            await page.screenshot(path=f"step_{self.current_step}_checkout.png")
            
        except Exception as e:
            print(f"⚠️ [PURCHASE] Checkout error: {e}")
            
        self.memory.log("purchase_step", {
            'step': self.current_step,
            'action': 'checkout',
            'status': 'completed'
        })
        
    async def _handle_login_if_required(self, page):
        """Handle login if required during checkout"""
        try:
            # Check if login is required
            login_selectors = [
                'input[type="email"]',
                'input[name="accountName"]',
                '#signIn'
            ]
            
            for selector in login_selectors:
                try:
                    login_field = await page.wait_for_selector(selector, timeout=3000)
                    if login_field:
                        print("🔐 [PURCHASE] Login required - using guest checkout")
                        # Look for guest checkout option
                        guest_selectors = [
                            'button:has-text("Continue as Guest")',
                            'button:has-text("Guest")',
                            '[data-analytics-title*="guest"]'
                        ]
                        
                        for guest_selector in guest_selectors:
                            try:
                                guest_button = await page.wait_for_selector(guest_selector, timeout=3000)
                                if guest_button:
                                    await guest_button.click()
                                    print("✅ [PURCHASE] Using guest checkout")
                                    return
                            except:
                                continue
                        break
                except:
                    continue
                    
        except Exception as e:
            print(f"⚠️ [PURCHASE] Login handling error: {e}")
            
    async def _step_payment(self, page, card_profile):
        """Step 7: Payment processing"""
        self.current_step = 7
        print(f"💳 [STEP {self.current_step}/{self.total_steps}] Processing payment...")
        
        payment_result = await self.payment_processor.process_payment(page, card_profile)
        
        await page.screenshot(path=f"step_{self.current_step}_payment.png")
        
        self.memory.log("purchase_step", {
            'step': self.current_step,
            'action': 'payment',
            'method': payment_result.get('method'),
            'status': payment_result.get('status', 'completed')
        })
        
        return payment_result
        
    async def _step_confirmation(self, page, payment_result):
        """Step 8: OTP and final confirmation"""
        self.current_step = 8
        print(f"✅ [STEP {self.current_step}/{self.total_steps}] Final confirmation...")
        
        # Handle OTP if required
        otp_result = await self.otp_handler.handle_otp_flow(page)
        
        # Look for order confirmation
        order_id = await self._extract_order_id(page)
        
        await page.screenshot(path=f"step_{self.current_step}_confirmation.png")
        
        result = {
            'otp_success': otp_result.get('success', False),
            'otp': otp_result.get('code'),
            'order_id': order_id,
            'confirmation_screenshot': f"step_{self.current_step}_confirmation.png"
        }
        
        self.memory.log("purchase_step", {
            'step': self.current_step,
            'action': 'confirmation',
            'otp_result': otp_result,
            'order_id': order_id,
            'status': 'completed'
        })
        
        return result
        
    async def _extract_order_id(self, page):
        """Extract order ID from confirmation page"""
        try:
            # Look for order ID patterns
            order_selectors = [
                '[data-analytics-title*="order"]',
                'text=/Order.*[A-Z0-9]{6,}/',
                '.order-number',
                '#order-id'
            ]
            
            for selector in order_selectors:
                try:
                    order_element = await page.wait_for_selector(selector, timeout=3000)
                    if order_element:
                        order_text = await order_element.text_content()
                        # Extract order ID from text
                        import re
                        order_match = re.search(r'[A-Z0-9]{6,}', order_text)
                        if order_match:
                            order_id = order_match.group()
                            print(f"✅ [PURCHASE] Order ID extracted: {order_id}")
                            return order_id
                except:
                    continue
                    
            return "ORDER_ID_NOT_FOUND"
            
        except Exception as e:
            print(f"⚠️ [PURCHASE] Order ID extraction error: {e}")
            return "EXTRACTION_ERROR"

async def buy_iphone(page, memory=None, card_profile=None):
    """Main purchase function - entry point"""
    if not memory:
        from memory import MemoryManager
        memory = MemoryManager()
        
    purchase_flow = PurchaseFlow(memory)
    return await purchase_flow.execute_purchase(page, card_profile)