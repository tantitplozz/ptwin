"""
🧠 GOD-TIER Memory Manager
Advanced VectorDB-like memory system for learning and optimization
"""

import json
import os
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from config import VECTORDB_PATH

class MemoryManager:
    def __init__(self):
        self.data = {
            'sessions': [],
            'patterns': {},
            'success_metrics': {},
            'failure_analysis': {},
            'optimization_data': {},
            'behavioral_patterns': {},
            'timing_analysis': {},
            'detection_events': [],
            'performance_metrics': {}
        }
        self.current_session = {
            'session_id': self._generate_session_id(),
            'start_time': datetime.now().isoformat(),
            'events': [],
            'metrics': {},
            'status': 'active'
        }
        self.load()
        
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        timestamp = datetime.now().isoformat()
        return hashlib.md5(timestamp.encode()).hexdigest()[:12]
        
    def load(self):
        """Load memory data from storage"""
        try:
            if os.path.exists(VECTORDB_PATH):
                with open(VECTORDB_PATH, "r", encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    self.data.update(loaded_data)
                print(f"🧠 [MEMORY] Loaded {len(self.data.get('sessions', []))} previous sessions")
            else:
                print("🧠 [MEMORY] Starting with fresh memory")
        except Exception as e:
            print(f"⚠️ [MEMORY] Load error: {e}")
            
    async def save(self):
        """Save memory data to storage"""
        try:
            # Finalize current session
            self.current_session['end_time'] = datetime.now().isoformat()
            self.current_session['status'] = 'completed'
            self.data['sessions'].append(self.current_session)
            
            # Clean old sessions (keep last 100)
            if len(self.data['sessions']) > 100:
                self.data['sessions'] = self.data['sessions'][-100:]
                
            # Save to file
            os.makedirs(os.path.dirname(VECTORDB_PATH), exist_ok=True)
            with open(VECTORDB_PATH, "w", encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
                
            print(f"🧠 [MEMORY] Saved session {self.current_session['session_id']}")
            
        except Exception as e:
            print(f"❌ [MEMORY] Save error: {e}")
            
    def log(self, event_type: str, data: Any):
        """Log event to current session"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': event_type,
            'data': data
        }
        self.current_session['events'].append(event)
        
        # Update patterns
        self._update_patterns(event_type, data)
        
    def _update_patterns(self, event_type: str, data: Any):
        """Update behavioral patterns"""
        if event_type not in self.data['patterns']:
            self.data['patterns'][event_type] = {
                'count': 0,
                'success_rate': 0.0,
                'avg_duration': 0.0,
                'common_errors': [],
                'optimization_hints': []
            }
            
        pattern = self.data['patterns'][event_type]
        pattern['count'] += 1
        
        # Analyze success/failure
        if isinstance(data, dict):
            if data.get('status') == 'success':
                pattern['success_rate'] = (pattern['success_rate'] * (pattern['count'] - 1) + 1) / pattern['count']
            elif data.get('status') == 'failed':
                pattern['success_rate'] = (pattern['success_rate'] * (pattern['count'] - 1)) / pattern['count']
                if 'error' in data:
                    pattern['common_errors'].append(data['error'])
                    
            # Track timing
            if 'duration' in data:
                pattern['avg_duration'] = (pattern['avg_duration'] * (pattern['count'] - 1) + data['duration']) / pattern['count']
                
    def get_success_patterns(self, event_type: str) -> Dict:
        """Get success patterns for specific event type"""
        return self.data['patterns'].get(event_type, {})
        
    def get_optimization_hints(self, event_type: str) -> List[str]:
        """Get optimization hints based on historical data"""
        pattern = self.data['patterns'].get(event_type, {})
        hints = []
        
        if pattern.get('success_rate', 0) < 0.5:
            hints.append(f"Low success rate ({pattern['success_rate']:.2%}) - consider strategy adjustment")
            
        if pattern.get('avg_duration', 0) > 30:
            hints.append(f"High average duration ({pattern['avg_duration']:.1f}s) - optimize timing")
            
        common_errors = pattern.get('common_errors', [])
        if common_errors:
            most_common = max(set(common_errors), key=common_errors.count)
            hints.append(f"Most common error: {most_common}")
            
        return hints
        
    def analyze_detection_risk(self) -> Dict:
        """Analyze detection risk based on historical data"""
        detection_events = self.data.get('detection_events', [])
        recent_detections = [
            event for event in detection_events
            if datetime.fromisoformat(event['timestamp']) > datetime.now() - timedelta(hours=24)
        ]
        
        risk_level = "LOW"
        if len(recent_detections) > 5:
            risk_level = "HIGH"
        elif len(recent_detections) > 2:
            risk_level = "MEDIUM"
            
        return {
            'risk_level': risk_level,
            'recent_detections': len(recent_detections),
            'total_detections': len(detection_events),
            'recommendations': self._get_risk_recommendations(risk_level)
        }
        
    def _get_risk_recommendations(self, risk_level: str) -> List[str]:
        """Get recommendations based on risk level"""
        if risk_level == "HIGH":
            return [
                "Consider using different GoLogin profile",
                "Increase warmup duration",
                "Add more random delays",
                "Switch proxy/location"
            ]
        elif risk_level == "MEDIUM":
            return [
                "Extend warmup phase",
                "Vary behavioral patterns",
                "Check proxy quality"
            ]
        else:
            return [
                "Continue current strategy",
                "Monitor for changes"
            ]
            
    def get_performance_metrics(self) -> Dict:
        """Get performance metrics"""
        sessions = self.data.get('sessions', [])
        if not sessions:
            return {}
            
        successful_sessions = [s for s in sessions if s.get('status') == 'completed']
        
        return {
            'total_sessions': len(sessions),
            'successful_sessions': len(successful_sessions),
            'success_rate': len(successful_sessions) / len(sessions) if sessions else 0,
            'avg_session_duration': self._calculate_avg_duration(sessions),
            'most_successful_patterns': self._get_most_successful_patterns()
        }
        
    def _calculate_avg_duration(self, sessions: List[Dict]) -> float:
        """Calculate average session duration"""
        durations = []
        for session in sessions:
            if 'start_time' in session and 'end_time' in session:
                try:
                    start = datetime.fromisoformat(session['start_time'])
                    end = datetime.fromisoformat(session['end_time'])
                    duration = (end - start).total_seconds()
                    durations.append(duration)
                except:
                    pass
                    
        return sum(durations) / len(durations) if durations else 0
        
    def _get_most_successful_patterns(self) -> List[Dict]:
        """Get most successful patterns"""
        patterns = []
        for event_type, pattern_data in self.data['patterns'].items():
            if pattern_data.get('success_rate', 0) > 0.7 and pattern_data.get('count', 0) > 3:
                patterns.append({
                    'event_type': event_type,
                    'success_rate': pattern_data['success_rate'],
                    'count': pattern_data['count']
                })
                
        return sorted(patterns, key=lambda x: x['success_rate'], reverse=True)[:5]
        
    def record_detection_event(self, detection_type: str, details: Dict):
        """Record detection event"""
        event = {
            'timestamp': datetime.now().isoformat(),
            'type': detection_type,
            'details': details,
            'session_id': self.current_session['session_id']
        }
        self.data['detection_events'].append(event)
        print(f"⚠️ [MEMORY] Detection event recorded: {detection_type}")
        
    def get_behavioral_recommendations(self) -> Dict:
        """Get behavioral recommendations based on memory"""
        recommendations = {
            'timing': self._get_timing_recommendations(),
            'patterns': self._get_pattern_recommendations(),
            'stealth': self._get_stealth_recommendations()
        }
        return recommendations
        
    def _get_timing_recommendations(self) -> List[str]:
        """Get timing-based recommendations"""
        timing_data = self.data.get('timing_analysis', {})
        recommendations = []
        
        # Analyze successful timing patterns
        successful_timings = [
            event for event in self.current_session['events']
            if event.get('data', {}).get('status') == 'success'
        ]
        
        if successful_timings:
            recommendations.append("Use timing patterns from successful sessions")
        else:
            recommendations.append("Increase random delays between actions")
            
        return recommendations
        
    def _get_pattern_recommendations(self) -> List[str]:
        """Get pattern-based recommendations"""
        return [
            "Vary mouse movement patterns",
            "Randomize scroll behavior",
            "Use different typing speeds"
        ]
        
    def _get_stealth_recommendations(self) -> List[str]:
        """Get stealth-based recommendations"""
        detection_risk = self.analyze_detection_risk()
        return detection_risk['recommendations']
        
    def export_analytics(self) -> Dict:
        """Export comprehensive analytics"""
        return {
            'session_analytics': self.get_performance_metrics(),
            'detection_analysis': self.analyze_detection_risk(),
            'behavioral_recommendations': self.get_behavioral_recommendations(),
            'pattern_analysis': self.data['patterns'],
            'current_session': self.current_session
        }