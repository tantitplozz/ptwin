"""
💳 GOD-TIER Payment Pattern Detection & Processing
Advanced payment method selection and form filling with stealth
"""

import random
import asyncio
import json
from datetime import datetime
from browser_stealth import simulate_human_behavior
from config import *

class PaymentProcessor:
    def __init__(self, memory_manager):
        self.memory = memory_manager
        self.payment_methods = {
            'credit_card': {
                'priority': 1,
                'success_rate': 0.85,
                'detection_risk': 'medium',
                'processing_time': 15
            },
            'apple_pay': {
                'priority': 2,
                'success_rate': 0.95,
                'detection_risk': 'low',
                'processing_time': 8
            },
            'promptpay': {
                'priority': 3,
                'success_rate': 0.90,
                'detection_risk': 'low',
                'processing_time': 12
            },
            'bank_transfer': {
                'priority': 4,
                'success_rate': 0.75,
                'detection_risk': 'high',
                'processing_time': 25
            }
        }
        
    async def process_payment(self, page, card_profile=None):
        """Process payment with intelligent method selection"""
        print("💳 [PAYMENT] Starting intelligent payment processing...")
        
        # Analyze available payment methods
        available_methods = await self._detect_available_methods(page)
        
        # Select optimal payment method
        selected_method = await self._select_optimal_method(available_methods, card_profile)
        
        # Process payment with selected method
        result = await self._execute_payment(page, selected_method, card_profile)
        
        # Log payment attempt
        self.memory.log("payment_attempt", {
            'method': selected_method,
            'available_methods': available_methods,
            'result': result,
            'timestamp': datetime.now().isoformat()
        })
        
        return result
        
    async def _detect_available_methods(self, page):
        """Detect available payment methods on page"""
        print("🔍 [PAYMENT] Detecting available payment methods...")
        
        available_methods = []
        
        # Check for Apple Pay
        apple_pay_selectors = [
            '[data-analytics-title*="apple pay"]',
            'button:has-text("Apple Pay")',
            '.apple-pay-button',
            '[aria-label*="Apple Pay"]'
        ]
        
        if await self._check_method_availability(page, apple_pay_selectors):
            available_methods.append('apple_pay')
            print("✅ [PAYMENT] Apple Pay available")
            
        # Check for Credit Card
        credit_card_selectors = [
            'input[name*="card"]',
            'input[placeholder*="card"]',
            '[data-analytics-title*="credit"]',
            '.credit-card-form'
        ]
        
        if await self._check_method_availability(page, credit_card_selectors):
            available_methods.append('credit_card')
            print("✅ [PAYMENT] Credit Card available")
            
        # Check for PromptPay
        promptpay_selectors = [
            '[data-analytics-title*="promptpay"]',
            'button:has-text("PromptPay")',
            '.promptpay-option'
        ]
        
        if await self._check_method_availability(page, promptpay_selectors):
            available_methods.append('promptpay')
            print("✅ [PAYMENT] PromptPay available")
            
        # Check for Bank Transfer
        bank_selectors = [
            '[data-analytics-title*="bank"]',
            'button:has-text("Bank Transfer")',
            '.bank-transfer-option'
        ]
        
        if await self._check_method_availability(page, bank_selectors):
            available_methods.append('bank_transfer')
            print("✅ [PAYMENT] Bank Transfer available")
            
        print(f"📊 [PAYMENT] Available methods: {available_methods}")
        return available_methods
        
    async def _check_method_availability(self, page, selectors):
        """Check if payment method is available"""
        for selector in selectors:
            try:
                element = await page.wait_for_selector(selector, timeout=2000)
                if element:
                    return True
            except:
                continue
        return False
        
    async def _select_optimal_method(self, available_methods, card_profile):
        """Select optimal payment method based on success patterns"""
        if not available_methods:
            print("⚠️ [PAYMENT] No payment methods detected, using credit_card as fallback")
            return 'credit_card'
            
        # Get historical success rates
        method_scores = {}
        for method in available_methods:
            base_score = self.payment_methods.get(method, {}).get('success_rate', 0.5)
            
            # Adjust based on historical data
            historical_pattern = self.memory.get_success_patterns(f"payment_{method}")
            if historical_pattern:
                historical_success = historical_pattern.get('success_rate', 0.5)
                # Weight: 70% historical, 30% base
                adjusted_score = (historical_success * 0.7) + (base_score * 0.3)
            else:
                adjusted_score = base_score
                
            # Adjust for detection risk
            detection_risk = self.memory.analyze_detection_risk()
            if detection_risk['risk_level'] == 'HIGH':
                # Prefer low-risk methods when detection risk is high
                risk_factor = self.payment_methods.get(method, {}).get('detection_risk', 'medium')
                if risk_factor == 'low':
                    adjusted_score *= 1.2
                elif risk_factor == 'high':
                    adjusted_score *= 0.8
                    
            method_scores[method] = adjusted_score
            
        # Select method with highest score
        optimal_method = max(method_scores, key=method_scores.get)
        print(f"🎯 [PAYMENT] Selected optimal method: {optimal_method} (score: {method_scores[optimal_method]:.2f})")
        
        return optimal_method
        
    async def _execute_payment(self, page, method, card_profile):
        """Execute payment with selected method"""
        print(f"💳 [PAYMENT] Executing payment with {method}...")
        
        start_time = datetime.now()
        
        try:
            if method == 'apple_pay':
                result = await self._process_apple_pay(page)
            elif method == 'credit_card':
                result = await self._process_credit_card(page, card_profile)
            elif method == 'promptpay':
                result = await self._process_promptpay(page)
            elif method == 'bank_transfer':
                result = await self._process_bank_transfer(page)
            else:
                result = await self._process_fallback_payment(page, card_profile)
                
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            result.update({
                'method': method,
                'duration': duration,
                'timestamp': end_time.isoformat()
            })
            
            return result
            
        except Exception as e:
            error_result = {
                'method': method,
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            print(f"❌ [PAYMENT] Error processing {method}: {e}")
            return error_result
            
    async def _process_apple_pay(self, page):
        """Process Apple Pay payment"""
        print("🍎 [PAYMENT] Processing Apple Pay...")
        
        try:
            # Click Apple Pay button
            apple_pay_selectors = [
                '[data-analytics-title*="apple pay"]',
                'button:has-text("Apple Pay")',
                '.apple-pay-button'
            ]
            
            for selector in apple_pay_selectors:
                try:
                    apple_pay_button = await page.wait_for_selector(selector, timeout=5000)
                    if apple_pay_button:
                        await apple_pay_button.click()
                        await asyncio.sleep(random.uniform(2, 4))
                        break
                except:
                    continue
                    
            # Simulate Apple Pay authentication (would require actual device)
            await asyncio.sleep(random.uniform(3, 6))
            
            # Check for success indicators
            success_indicators = [
                'text="Payment Successful"',
                'text="Order Confirmed"',
                '.payment-success'
            ]
            
            for indicator in success_indicators:
                try:
                    success_element = await page.wait_for_selector(indicator, timeout=5000)
                    if success_element:
                        return {'status': 'success', 'method': 'apple_pay'}
                except:
                    continue
                    
            return {'status': 'pending', 'method': 'apple_pay'}
            
        except Exception as e:
            return {'status': 'failed', 'method': 'apple_pay', 'error': str(e)}
            
    async def _process_credit_card(self, page, card_profile):
        """Process credit card payment"""
        print("💳 [PAYMENT] Processing credit card...")
        
        try:
            # Fill credit card form
            await self._fill_credit_card_form(page, card_profile)
            
            # Submit payment
            submit_selectors = [
                'button:has-text("Place Order")',
                'button:has-text("Complete Purchase")',
                'button:has-text("Pay Now")',
                '[data-analytics-title*="place order"]'
            ]
            
            for selector in submit_selectors:
                try:
                    submit_button = await page.wait_for_selector(selector, timeout=5000)
                    if submit_button:
                        await submit_button.click()
                        await asyncio.sleep(random.uniform(3, 6))
                        break
                except:
                    continue
                    
            return {'status': 'submitted', 'method': 'credit_card'}
            
        except Exception as e:
            return {'status': 'failed', 'method': 'credit_card', 'error': str(e)}
            
    async def _fill_credit_card_form(self, page, card_profile):
        """Fill credit card form with human-like behavior"""
        print("📝 [PAYMENT] Filling credit card form...")
        
        # Card number
        card_number = PAYMENT_CARD_NUMBER or "4111111111111111"  # Test card
        await self._fill_field_naturally(page, [
            'input[name*="card"]',
            'input[placeholder*="card number"]',
            '#card-number'
        ], card_number)
        
        # Expiry date
        expiry = PAYMENT_EXP or "12/29"
        await self._fill_field_naturally(page, [
            'input[name*="expir"]',
            'input[placeholder*="MM/YY"]',
            '#expiry-date'
        ], expiry)
        
        # CVV
        cvv = PAYMENT_CVV or "123"
        await self._fill_field_naturally(page, [
            'input[name*="cvv"]',
            'input[name*="cvc"]',
            'input[placeholder*="security"]',
            '#cvv'
        ], cvv)
        
        # Cardholder name
        name = PAYMENT_NAME or "John Doe"
        await self._fill_field_naturally(page, [
            'input[name*="name"]',
            'input[placeholder*="name"]',
            '#cardholder-name'
        ], name)
        
        print("✅ [PAYMENT] Credit card form filled")
        
    async def _fill_field_naturally(self, page, selectors, value):
        """Fill form field with natural human typing"""
        for selector in selectors:
            try:
                field = await page.wait_for_selector(selector, timeout=3000)
                if field:
                    await field.click()
                    await asyncio.sleep(random.uniform(0.5, 1.0))
                    
                    # Clear field
                    await field.clear()
                    
                    # Type naturally
                    for char in value:
                        await field.type(char)
                        await asyncio.sleep(random.uniform(0.05, 0.15))
                        
                    await asyncio.sleep(random.uniform(0.3, 0.8))
                    return True
            except:
                continue
        return False
        
    async def _process_promptpay(self, page):
        """Process PromptPay payment"""
        print("📱 [PAYMENT] Processing PromptPay...")
        
        try:
            # Click PromptPay option
            promptpay_selectors = [
                '[data-analytics-title*="promptpay"]',
                'button:has-text("PromptPay")',
                '.promptpay-option'
            ]
            
            for selector in promptpay_selectors:
                try:
                    promptpay_button = await page.wait_for_selector(selector, timeout=5000)
                    if promptpay_button:
                        await promptpay_button.click()
                        await asyncio.sleep(random.uniform(2, 4))
                        break
                except:
                    continue
                    
            # Wait for QR code or payment instructions
            await asyncio.sleep(random.uniform(5, 8))
            
            return {'status': 'pending', 'method': 'promptpay'}
            
        except Exception as e:
            return {'status': 'failed', 'method': 'promptpay', 'error': str(e)}
            
    async def _process_bank_transfer(self, page):
        """Process bank transfer payment"""
        print("🏦 [PAYMENT] Processing bank transfer...")
        
        try:
            # Click bank transfer option
            bank_selectors = [
                '[data-analytics-title*="bank"]',
                'button:has-text("Bank Transfer")',
                '.bank-transfer-option'
            ]
            
            for selector in bank_selectors:
                try:
                    bank_button = await page.wait_for_selector(selector, timeout=5000)
                    if bank_button:
                        await bank_button.click()
                        await asyncio.sleep(random.uniform(2, 4))
                        break
                except:
                    continue
                    
            return {'status': 'pending', 'method': 'bank_transfer'}
            
        except Exception as e:
            return {'status': 'failed', 'method': 'bank_transfer', 'error': str(e)}
            
    async def _process_fallback_payment(self, page, card_profile):
        """Fallback payment processing"""
        print("🔄 [PAYMENT] Using fallback payment method...")
        
        # Try to find any payment button and click it
        fallback_selectors = [
            'button:has-text("Pay")',
            'button:has-text("Order")',
            'button:has-text("Purchase")',
            '.payment-button',
            '.checkout-button'
        ]
        
        for selector in fallback_selectors:
            try:
                button = await page.wait_for_selector(selector, timeout=3000)
                if button:
                    await button.click()
                    await asyncio.sleep(random.uniform(2, 4))
                    return {'status': 'submitted', 'method': 'fallback'}
            except:
                continue
                
        return {'status': 'failed', 'method': 'fallback', 'error': 'No payment method found'}