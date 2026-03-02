"""
🏆 REVOLUTIONARY: User Fatigue Protection
Protects long-term user experience by detecting and preventing recommendation fatigue
"""

import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Optional
import redis
import json
import yaml


class FatigueProtector:
    """
    Detects and prevents recommendation fatigue
    
    Key Innovation:
    - Traditional: Always show recommendations
    - Our System: Adaptive based on user response patterns
    
    Features:
    1. Rejection tracking
    2. Adaptive aggressiveness
    3. Cooldown periods
    4. Long-term trust protection
    """
    
    def __init__(self, config_path="config.yaml", redis_client=None):
        with open(config_path, encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        self.config = config['fatigue']
        self.redis_config = config['redis']
        
        print("\n" + "="*70)
        print("🏆 USER FATIGUE PROTECTOR")
        print("="*70)
        print("\n🛡️  Revolutionary Feature: Long-term User Experience Protection")
        print(f"   Rejection Threshold: {self.config['rejection_threshold']}")
        print(f"   Cooldown Period: {self.config['cooldown_period']}s")
        print(f"   Adaptive Aggressiveness: {self.config['min_aggressiveness']:.0%} - {self.config['max_aggressiveness']:.0%}")
        
        # Redis for state tracking
        self.redis_client = redis_client
        if self.redis_client is None:
            try:
                self.redis_client = redis.Redis(
                    host=self.redis_config['host'],
                    port=self.redis_config['port'],
                    db=self.redis_config['db'],
                    decode_responses=True
                )
                self.redis_client.ping()
                print("   ✅ Redis connected for fatigue tracking")
            except:
                print("   ⚠️  Redis not available - using in-memory tracking")
                self.redis_client = None
                self.memory_store = {}
    
    def get_user_state(self, user_id: int) -> Dict:
        """Get user's fatigue state"""
        
        key = f"{self.redis_config['fatigue_state_prefix']}{user_id}"
        
        if self.redis_client:
            state_json = self.redis_client.get(key)
            if state_json:
                return json.loads(state_json)
        else:
            if user_id in self.memory_store:
                return self.memory_store[user_id]
        
        # Default state
        return {
            'consecutive_rejections': 0,
            'total_recommendations': 0,
            'total_acceptances': 0,
            'last_rejection_time': None,
            'in_cooldown': False,
            'aggressiveness': self.config['max_aggressiveness']
        }
    
    def update_user_state(self, user_id: int, state: Dict):
        """Update user's fatigue state"""
        
        key = f"{self.redis_config['fatigue_state_prefix']}{user_id}"
        
        if self.redis_client:
            self.redis_client.setex(
                key,
                86400,  # 24 hours TTL
                json.dumps(state)
            )
        else:
            self.memory_store[user_id] = state
    
    def record_recommendation(
        self,
        user_id: int,
        accepted: bool,
        timestamp: Optional[datetime] = None
    ):
        """
        Record recommendation outcome
        
        Args:
            user_id: User ID
            accepted: Whether recommendation was accepted
            timestamp: When it happened (default: now)
        """
        
        if timestamp is None:
            timestamp = datetime.now()
        
        state = self.get_user_state(user_id)
        
        state['total_recommendations'] += 1
        
        if accepted:
            # Reset rejection counter on acceptance
            state['consecutive_rejections'] = 0
            state['total_acceptances'] += 1
            state['in_cooldown'] = False
            
            # Increase aggressiveness (user is responsive)
            state['aggressiveness'] = min(
                state['aggressiveness'] + 0.1,
                self.config['max_aggressiveness']
            )
            
        else:
            # Increment rejection counter
            state['consecutive_rejections'] += 1
            state['last_rejection_time'] = timestamp.isoformat()
            
            # Check if threshold exceeded
            if state['consecutive_rejections'] >= self.config['rejection_threshold']:
                state['in_cooldown'] = True
                
                # Decrease aggressiveness
                state['aggressiveness'] = max(
                    state['aggressiveness'] * (1 - self.config['decay_rate']),
                    self.config['min_aggressiveness']
                )
        
        self.update_user_state(user_id, state)
    
    def should_show_recommendation(
        self,
        user_id: int,
        current_time: Optional[datetime] = None
    ) -> Dict[str, any]:
        """
        Decide whether to show recommendation
        
        Returns:
            {
                'show': bool,
                'reason': str,
                'aggressiveness': float,
                'in_cooldown': bool
            }
        """
        
        if current_time is None:
            current_time = datetime.now()
        
        state = self.get_user_state(user_id)
        
        # Check cooldown
        if state['in_cooldown'] and state['last_rejection_time']:
            last_rejection = datetime.fromisoformat(state['last_rejection_time'])
            time_since_rejection = (current_time - last_rejection).total_seconds()
            
            if time_since_rejection < self.config['cooldown_period']:
                return {
                    'show': False,
                    'reason': 'user_in_cooldown',
                    'aggressiveness': state['aggressiveness'],
                    'in_cooldown': True,
                    'cooldown_remaining': self.config['cooldown_period'] - time_since_rejection
                }
            else:
                # Cooldown expired
                state['in_cooldown'] = False
                state['consecutive_rejections'] = 0
                self.update_user_state(user_id, state)
        
        # Probabilistic showing based on aggressiveness
        show_probability = state['aggressiveness']
        show = np.random.random() < show_probability
        
        return {
            'show': show,
            'reason': 'adaptive_probability' if not show else 'normal',
            'aggressiveness': state['aggressiveness'],
            'in_cooldown': False,
            'show_probability': show_probability
        }
    
    def get_user_metrics(self, user_id: int) -> Dict:
        """Get user fatigue metrics"""
        
        state = self.get_user_state(user_id)
        
        acceptance_rate = (
            state['total_acceptances'] / state['total_recommendations']
            if state['total_recommendations'] > 0
            else 0.0
        )
        
        return {
            'user_id': user_id,
            'total_recommendations': state['total_recommendations'],
            'total_acceptances': state['total_acceptances'],
            'acceptance_rate': acceptance_rate,
            'consecutive_rejections': state['consecutive_rejections'],
            'current_aggressiveness': state['aggressiveness'],
            'in_cooldown': state['in_cooldown'],
            'fatigue_level': self._calculate_fatigue_level(state)
        }
    
    def _calculate_fatigue_level(self, state: Dict) -> str:
        """Calculate fatigue level"""
        
        if state['in_cooldown']:
            return 'high'
        elif state['consecutive_rejections'] >= 2:
            return 'medium'
        elif state['aggressiveness'] < 0.5:
            return 'medium'
        else:
            return 'low'
    
    def adjust_recommendation_count(
        self,
        user_id: int,
        base_count: int
    ) -> int:
        """
        Adjust number of recommendations based on fatigue
        
        Args:
            user_id: User ID
            base_count: Base number of recommendations
        
        Returns:
            Adjusted count
        """
        
        state = self.get_user_state(user_id)
        
        # Reduce count based on aggressiveness
        adjusted_count = int(base_count * state['aggressiveness'])
        
        # Minimum 1 if showing at all
        return max(1, adjusted_count)
    
    def get_global_metrics(self) -> Dict:
        """Get global fatigue metrics across all users"""
        
        # This would aggregate across all users
        # For now, return placeholder
        return {
            'total_users_tracked': len(self.memory_store) if not self.redis_client else 'N/A',
            'users_in_cooldown': 0,  # Would count from Redis
            'avg_aggressiveness': 0.7,  # Would calculate from Redis
            'fatigue_protection_active': self.config['enabled']
        }


if __name__ == "__main__":
    print("🏆 User Fatigue Protector - Revolutionary Module")
    print("   First system to protect long-term user experience!")
    
    # Demo
    protector = FatigueProtector()
    
    # Simulate user interactions
    user_id = 123
    
    print("\n📊 Simulating user interactions...")
    
    # First few recommendations - accepted
    for i in range(3):
        decision = protector.should_show_recommendation(user_id)
        print(f"\n   Recommendation {i+1}: {decision}")
        protector.record_recommendation(user_id, accepted=True)
    
    # Then rejections
    for i in range(4):
        decision = protector.should_show_recommendation(user_id)
        print(f"\n   Recommendation {i+4}: {decision}")
        protector.record_recommendation(user_id, accepted=False)
    
    # Check metrics
    metrics = protector.get_user_metrics(user_id)
    print(f"\n📈 User Metrics: {metrics}")
