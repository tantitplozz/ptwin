"""
🧪 GOD-TIER A/B Testing System
Advanced multi-profile testing and optimization
"""

import random
import asyncio
import json
from datetime import datetime
from config import AB_TEST_PROFILES, AB_TEST_ITERATIONS

class ABTestRunner:
    def __init__(self, memory_manager):
        self.memory = memory_manager
        self.test_profiles = self._generate_test_profiles()
        self.current_test_session = {
            'session_id': self._generate_test_id(),
            'start_time': datetime.now(),
            'profiles_tested': [],
            'results': [],
            'best_profile': None
        }
        
    def _generate_test_id(self):
        """Generate unique test session ID"""
        import hashlib
        timestamp = datetime.now().isoformat()
        return f"AB_{hashlib.md5(timestamp.encode()).hexdigest()[:8]}"
        
    def _generate_test_profiles(self):
        """Generate diverse test profiles for A/B testing"""
        profiles = []
        
        # Profile A: Conservative (Low risk, high stealth)
        profiles.append({
            'name': 'Conservative',
            'id': 'profile_a',
            'characteristics': {
                'speed': 'slow',
                'stealth_level': 'maximum',
                'risk_tolerance': 'low',
                'human_simulation': 'high',
                'delay_multiplier': 2.0,
                'error_recovery': 'cautious'
            },
            'timing': {
                'page_load_wait': (5, 10),
                'action_delay': (2, 5),
                'typing_speed': (0.1, 0.3),
                'mouse_movement': 'slow'
            },
            'behavior': {
                'scroll_pattern': 'natural',
                'click_precision': 'human',
                'form_filling': 'gradual',
                'error_handling': 'retry_with_delay'
            }
        })
        
        # Profile B: Balanced (Medium risk, balanced performance)
        profiles.append({
            'name': 'Balanced',
            'id': 'profile_b',
            'characteristics': {
                'speed': 'medium',
                'stealth_level': 'high',
                'risk_tolerance': 'medium',
                'human_simulation': 'medium',
                'delay_multiplier': 1.5,
                'error_recovery': 'adaptive'
            },
            'timing': {
                'page_load_wait': (3, 7),
                'action_delay': (1, 3),
                'typing_speed': (0.05, 0.2),
                'mouse_movement': 'medium'
            },
            'behavior': {
                'scroll_pattern': 'varied',
                'click_precision': 'accurate',
                'form_filling': 'steady',
                'error_handling': 'smart_retry'
            }
        })
        
        # Profile C: Aggressive (Higher risk, faster execution)
        profiles.append({
            'name': 'Aggressive',
            'id': 'profile_c',
            'characteristics': {
                'speed': 'fast',
                'stealth_level': 'medium',
                'risk_tolerance': 'high',
                'human_simulation': 'low',
                'delay_multiplier': 1.0,
                'error_recovery': 'quick'
            },
            'timing': {
                'page_load_wait': (2, 4),
                'action_delay': (0.5, 2),
                'typing_speed': (0.02, 0.1),
                'mouse_movement': 'fast'
            },
            'behavior': {
                'scroll_pattern': 'direct',
                'click_precision': 'precise',
                'form_filling': 'rapid',
                'error_handling': 'immediate_retry'
            }
        })
        
        # Add custom profiles based on historical data
        historical_profiles = self._generate_historical_profiles()
        profiles.extend(historical_profiles)
        
        return profiles[:AB_TEST_PROFILES]
        
    def _generate_historical_profiles(self):
        """Generate profiles based on historical success patterns"""
        profiles = []
        
        # Get historical success patterns from memory
        historical_data = self.memory.get_performance_metrics()
        successful_patterns = self.memory._get_most_successful_patterns()
        
        if successful_patterns:
            # Create profile based on most successful pattern
            best_pattern = successful_patterns[0]
            profiles.append({
                'name': 'Historical_Best',
                'id': 'profile_historical',
                'characteristics': {
                    'speed': 'adaptive',
                    'stealth_level': 'maximum',
                    'risk_tolerance': 'low',
                    'human_simulation': 'high',
                    'delay_multiplier': 1.8,
                    'error_recovery': 'pattern_based'
                },
                'timing': {
                    'page_load_wait': (4, 8),
                    'action_delay': (1.5, 4),
                    'typing_speed': (0.08, 0.25),
                    'mouse_movement': 'natural'
                },
                'behavior': {
                    'scroll_pattern': 'learned',
                    'click_precision': 'optimized',
                    'form_filling': 'pattern_based',
                    'error_handling': 'historical_best'
                },
                'success_rate': best_pattern.get('success_rate', 0.0)
            })
            
        return profiles
        
    async def run_flows(self, page, flow_function):
        """Run A/B testing with multiple profiles"""
        print(f"🧪 [A/B TEST] Starting test session: {self.current_test_session['session_id']}")
        print(f"🧪 [A/B TEST] Testing {len(self.test_profiles)} profiles")
        
        results = []
        
        for i, profile in enumerate(self.test_profiles):
            print(f"🧪 [A/B TEST] Testing profile {i+1}/{len(self.test_profiles)}: {profile['name']}")
            
            # Apply profile settings
            await self._apply_profile_settings(page, profile)
            
            # Run test iterations for this profile
            profile_results = []
            for iteration in range(AB_TEST_ITERATIONS):
                print(f"🔄 [A/B TEST] Profile {profile['name']} - Iteration {iteration+1}/{AB_TEST_ITERATIONS}")
                
                try:
                    # Execute flow with current profile
                    start_time = datetime.now()
                    result = await flow_function(page, self.memory, profile)
                    end_time = datetime.now()
                    
                    # Calculate metrics
                    duration = (end_time - start_time).total_seconds()
                    success = result.get('status') == 'success'
                    
                    iteration_result = {
                        'iteration': iteration + 1,
                        'success': success,
                        'duration': duration,
                        'result': result,
                        'timestamp': end_time.isoformat()
                    }
                    
                    profile_results.append(iteration_result)
                    
                    # Log to memory
                    self.memory.log("ab_test_iteration", {
                        'profile': profile['name'],
                        'iteration': iteration + 1,
                        'result': iteration_result
                    })
                    
                    # Wait between iterations
                    if iteration < AB_TEST_ITERATIONS - 1:
                        await asyncio.sleep(random.uniform(2, 5))
                        
                except Exception as e:
                    print(f"❌ [A/B TEST] Error in profile {profile['name']}, iteration {iteration+1}: {e}")
                    profile_results.append({
                        'iteration': iteration + 1,
                        'success': False,
                        'duration': 0,
                        'error': str(e),
                        'timestamp': datetime.now().isoformat()
                    })
                    
            # Analyze profile performance
            profile_analysis = self._analyze_profile_performance(profile, profile_results)
            results.append(profile_analysis)
            
            self.current_test_session['profiles_tested'].append(profile['name'])
            self.current_test_session['results'].append(profile_analysis)
            
            print(f"📊 [A/B TEST] Profile {profile['name']} completed - Success rate: {profile_analysis['success_rate']:.1%}")
            
        # Determine best profile
        best_profile = self._select_best_profile(results)
        self.current_test_session['best_profile'] = best_profile
        
        # Log complete test session
        self.memory.log("ab_test_session", self.current_test_session)
        
        print(f"🏆 [A/B TEST] Best profile: {best_profile['profile']['name']} (Score: {best_profile['overall_score']:.2f})")
        
        return best_profile
        
    async def _apply_profile_settings(self, page, profile):
        """Apply profile-specific settings to browser/page"""
        print(f"⚙️ [A/B TEST] Applying settings for profile: {profile['name']}")
        
        # Store profile settings in page context for use by other modules
        await page.evaluate(f"""
            window.currentProfile = {json.dumps(profile)};
        """)
        
        # Apply timing settings (these would be used by other modules)
        timing = profile.get('timing', {})
        characteristics = profile.get('characteristics', {})
        
        # Set global timing multiplier
        delay_multiplier = characteristics.get('delay_multiplier', 1.0)
        await page.evaluate(f"""
            window.delayMultiplier = {delay_multiplier};
        """)
        
        print(f"✅ [A/B TEST] Profile {profile['name']} settings applied")
        
    def _analyze_profile_performance(self, profile, results):
        """Analyze performance of a specific profile"""
        if not results:
            return {
                'profile': profile,
                'success_rate': 0.0,
                'avg_duration': 0.0,
                'error_rate': 1.0,
                'overall_score': 0.0,
                'iterations': 0
            }
            
        successful_results = [r for r in results if r.get('success', False)]
        
        success_rate = len(successful_results) / len(results)
        avg_duration = sum(r.get('duration', 0) for r in results) / len(results)
        error_rate = 1 - success_rate
        
        # Calculate overall score (weighted combination of metrics)
        speed_score = max(0, 1 - (avg_duration / 60))  # Normalize to 60 seconds max
        success_score = success_rate
        stealth_score = self._calculate_stealth_score(profile, results)
        
        # Weighted scoring
        overall_score = (
            success_score * 0.5 +      # 50% weight on success
            speed_score * 0.3 +        # 30% weight on speed
            stealth_score * 0.2        # 20% weight on stealth
        )
        
        return {
            'profile': profile,
            'success_rate': success_rate,
            'avg_duration': avg_duration,
            'error_rate': error_rate,
            'speed_score': speed_score,
            'stealth_score': stealth_score,
            'overall_score': overall_score,
            'iterations': len(results),
            'successful_iterations': len(successful_results),
            'results': results
        }
        
    def _calculate_stealth_score(self, profile, results):
        """Calculate stealth score based on profile characteristics and results"""
        stealth_level = profile.get('characteristics', {}).get('stealth_level', 'medium')
        
        # Base stealth score from profile
        stealth_scores = {
            'maximum': 1.0,
            'high': 0.8,
            'medium': 0.6,
            'low': 0.4
        }
        
        base_score = stealth_scores.get(stealth_level, 0.6)
        
        # Adjust based on detection events (would be tracked in real implementation)
        detection_penalty = 0  # Placeholder for actual detection tracking
        
        return max(0, base_score - detection_penalty)
        
    def _select_best_profile(self, results):
        """Select the best performing profile"""
        if not results:
            return None
            
        # Sort by overall score
        sorted_results = sorted(results, key=lambda x: x['overall_score'], reverse=True)
        best_result = sorted_results[0]
        
        # Add additional context
        best_result['rank'] = 1
        best_result['improvement_over_worst'] = (
            best_result['overall_score'] - sorted_results[-1]['overall_score']
        ) if len(sorted_results) > 1 else 0
        
        return best_result
        
    def get_test_summary(self):
        """Get summary of current test session"""
        return {
            'session_id': self.current_test_session['session_id'],
            'start_time': self.current_test_session['start_time'].isoformat(),
            'profiles_tested': len(self.current_test_session['profiles_tested']),
            'total_iterations': len(self.current_test_session['results']) * AB_TEST_ITERATIONS,
            'best_profile': self.current_test_session.get('best_profile', {}).get('profile', {}).get('name'),
            'best_score': self.current_test_session.get('best_profile', {}).get('overall_score', 0)
        }
        
    def export_test_results(self):
        """Export detailed test results"""
        return {
            'test_session': self.current_test_session,
            'profiles': self.test_profiles,
            'detailed_results': self.current_test_session['results'],
            'summary': self.get_test_summary(),
            'recommendations': self._generate_recommendations()
        }
        
    def _generate_recommendations(self):
        """Generate recommendations based on test results"""
        recommendations = []
        
        if not self.current_test_session['results']:
            return ["No test results available for recommendations"]
            
        best_profile = self.current_test_session.get('best_profile')
        if not best_profile:
            return ["Unable to determine best profile"]
            
        # Analyze best profile characteristics
        best_characteristics = best_profile['profile'].get('characteristics', {})
        
        if best_characteristics.get('speed') == 'slow':
            recommendations.append("Slower execution speeds show better results - prioritize stealth over speed")
            
        if best_characteristics.get('stealth_level') == 'maximum':
            recommendations.append("Maximum stealth settings are optimal for this target")
            
        if best_profile['success_rate'] < 0.7:
            recommendations.append("Consider additional warmup time or different approach")
            
        if best_profile['avg_duration'] > 120:
            recommendations.append("Process is taking longer than expected - investigate bottlenecks")
            
        return recommendations