"""
Revolutionary Data Generator with Causal Structure
Generates data with TRUE causal effects for proper evaluation
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import yaml
from pathlib import Path
from tqdm import tqdm


class CausalDataGenerator:
    """Generate data with explicit causal structure"""
    
    def __init__(self, config_path="config.yaml"):
        with open(config_path, encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.data_config = self.config['data']
        self.causal_config = self.config['causal']
        
        np.random.seed(self.data_config['seed'])
        
        print("\n" + "="*70)
        print("🏆 CAUSAL REVENUE-OPTIMIZED DATA GENERATOR")
        print("="*70)
        print("\n🎯 Generating data with TRUE causal structure...")
        print(f"   Treatment Effect: {self.data_config['treatment_effect']:.1%}")
        print(f"   Confounding: {self.data_config['confounding_strength']:.1%}")
    
    def generate_all(self):
        """Generate complete dataset with causal structure"""
        
        # Create output directory
        output_dir = Path(self.config['paths']['data_dir'])
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate components
        print("\n📊 Generating components...")
        
        users_df = self._generate_users()
        items_df = self._generate_items()
        restaurants_df = self._generate_restaurants()
        orders_df = self._generate_orders_with_causality(users_df, items_df)
        
        # Save
        print("\n💾 Saving data...")
        users_df.to_parquet(output_dir / "users.parquet")
        items_df.to_parquet(output_dir / "items.parquet")
        restaurants_df.to_parquet(output_dir / "restaurants.parquet")
        orders_df.to_parquet(output_dir / "orders.parquet")
        
        print("\n✅ Data generation complete!")
        print(f"\n📈 Statistics:")
        print(f"   Users: {len(users_df):,}")
        print(f"   Items: {len(items_df):,}")
        print(f"   Restaurants: {len(restaurants_df):,}")
        print(f"   Orders: {len(orders_df):,}")
        print(f"\n💰 Causal Structure:")
        print(f"   True Treatment Effect: ₹{self.data_config['treatment_effect'] * 450:.2f}")
        print(f"   Confounding Bias: {self.data_config['confounding_strength']:.1%}")
        
        return users_df, items_df, restaurants_df, orders_df
    
    def _generate_users(self):
        """Generate users with behavioral segments"""
        n = self.data_config['n_users']
        
        print(f"   👥 Generating {n:,} users...")
        
        # User segments (affects both treatment and outcome - confounding!)
        segments = np.random.choice(
            ['budget', 'regular', 'premium', 'vip'],
            size=n,
            p=[0.3, 0.4, 0.2, 0.1]
        )
        
        # Segment characteristics
        segment_map = {
            'budget': {'base_aov': 250, 'responsiveness': 0.3, 'fatigue_threshold': 2},
            'regular': {'base_aov': 450, 'responsiveness': 0.5, 'fatigue_threshold': 3},
            'premium': {'base_aov': 750, 'responsiveness': 0.7, 'fatigue_threshold': 4},
            'vip': {'base_aov': 1200, 'responsiveness': 0.9, 'fatigue_threshold': 5}
        }
        
        users = []
        for i in tqdm(range(n), desc="Users"):
            segment = segments[i]
            char = segment_map[segment]
            
            users.append({
                'user_id': i,
                'segment': segment,
                'base_aov': char['base_aov'] + np.random.normal(0, 50),
                'responsiveness': char['responsiveness'] + np.random.normal(0, 0.1),
                'price_sensitivity': np.random.beta(2, 5),
                'fatigue_threshold': char['fatigue_threshold'],
                'order_frequency': np.random.poisson(5) + 1,
                'avg_cart_size': np.random.poisson(3) + 1,
                'created_at': datetime.now() - timedelta(days=np.random.randint(1, 365))
            })
        
        return pd.DataFrame(users)
    
    def _generate_items(self):
        """Generate items with profit margins"""
        n = self.data_config['n_items']
        
        print(f"   🍽️  Generating {n:,} items...")
        
        cuisines = ['North Indian', 'South Indian', 'Chinese', 'Italian', 
                   'Continental', 'Fast Food', 'Desserts', 'Beverages']
        
        meal_types = ['Breakfast', 'Lunch', 'Dinner', 'Snacks']
        
        categories = ['Main Course', 'Starter', 'Bread', 'Rice', 'Dessert', 
                     'Beverage', 'Salad', 'Combo']
        
        items = []
        for i in tqdm(range(n), desc="Items"):
            cuisine = np.random.choice(cuisines)
            meal_type = np.random.choice(meal_types)
            category = np.random.choice(categories)
            
            # Base price depends on category
            category_prices = {
                'Main Course': (200, 400),
                'Starter': (100, 200),
                'Bread': (30, 80),
                'Rice': (150, 250),
                'Dessert': (80, 150),
                'Beverage': (40, 100),
                'Salad': (80, 150),
                'Combo': (300, 600)
            }
            
            price_range = category_prices[category]
            price = np.random.uniform(*price_range)
            
            # Profit margin (CRITICAL for profit optimization!)
            margin_range = self.data_config['profit_margin_range']
            profit_margin = np.random.uniform(*margin_range)
            
            # Popularity (affects confounding)
            popularity = np.random.lognormal(0, 1)
            
            items.append({
                'item_id': i,
                'item_name': f"{cuisine} {category} {i}",
                'cuisine': cuisine,
                'meal_type': meal_type,
                'category': category,
                'price': round(price, 2),
                'profit_margin': round(profit_margin, 3),
                'profit_amount': round(price * profit_margin, 2),
                'popularity': popularity,
                'restaurant_id': np.random.randint(0, self.data_config['n_restaurants']),
                'description': f"Delicious {cuisine} {category} for {meal_type}"
            })
        
        return pd.DataFrame(items)
    
    def _generate_restaurants(self):
        """Generate restaurants"""
        n = self.data_config['n_restaurants']
        
        print(f"   🏪 Generating {n:,} restaurants...")
        
        restaurants = []
        for i in range(n):
            restaurants.append({
                'restaurant_id': i,
                'restaurant_name': f"Restaurant {i}",
                'rating': round(np.random.uniform(3.0, 5.0), 1),
                'avg_delivery_time': np.random.randint(20, 60),
                'commission_rate': round(np.random.uniform(0.15, 0.30), 2)
            })
        
        return pd.DataFrame(restaurants)
    
    def _generate_orders_with_causality(self, users_df, items_df):
        """
        Generate orders with EXPLICIT causal structure
        
        Causal Model:
        - Confounders (C): user_segment, time_of_day, cart_value
        - Treatment (T): recommendation_shown
        - Outcome (Y): order_value, profit
        
        True causal effect: E[Y|do(T=1)] - E[Y|do(T=0)]
        """
        n = self.data_config['n_orders']
        
        print(f"   📦 Generating {n:,} orders with causal structure...")
        
        treatment_effect = self.data_config['treatment_effect']
        confounding = self.data_config['confounding_strength']
        
        orders = []
        
        for i in tqdm(range(n), desc="Orders"):
            # Select user
            user = users_df.sample(1).iloc[0]
            
            # Confounders
            hour = np.random.randint(0, 24)
            is_peak = 1 if hour in [12, 13, 19, 20, 21] else 0
            is_weekend = np.random.random() < 0.29  # ~2/7 days
            
            # Base cart (before recommendation)
            n_items = np.random.poisson(user['avg_cart_size']) + 1
            cart_items = items_df.sample(n_items)
            base_cart_value = cart_items['price'].sum()
            
            # Propensity to receive recommendation (confounded!)
            # Higher for premium users, peak times, larger carts
            propensity_score = 0.5  # Base
            propensity_score += 0.2 * (user['segment'] in ['premium', 'vip'])
            propensity_score += 0.1 * is_peak
            propensity_score += 0.1 * (base_cart_value > 500)
            propensity_score += confounding * np.random.normal(0, 0.1)
            propensity_score = np.clip(propensity_score, 0.1, 0.9)
            
            # Treatment assignment (recommendation shown)
            recommendation_shown = np.random.random() < propensity_score
            
            # Outcome (order value)
            # Base outcome (affected by confounders)
            expected_value = base_cart_value
            expected_value *= (1 + 0.1 * (user['segment'] == 'premium'))
            expected_value *= (1 + 0.05 * is_peak)
            
            # TRUE CAUSAL EFFECT (only if recommendation shown AND accepted)
            if recommendation_shown:
                # Acceptance probability
                acceptance_prob = user['responsiveness']
                acceptance_prob *= (1 - user['price_sensitivity'] * 0.3)
                
                recommendation_accepted = np.random.random() < acceptance_prob
                
                if recommendation_accepted:
                    # TRUE treatment effect!
                    recommended_item = items_df.sample(1).iloc[0]
                    incremental_value = recommended_item['price']
                    incremental_profit = recommended_item['profit_amount']
                    
                    # Apply true causal effect
                    expected_value += incremental_value * (1 + treatment_effect)
                else:
                    recommendation_accepted = False
                    incremental_value = 0
                    incremental_profit = 0
            else:
                recommendation_accepted = False
                incremental_value = 0
                incremental_profit = 0
            
            # Add noise
            final_value = expected_value + np.random.normal(0, 30)
            final_value = max(final_value, base_cart_value)  # Can't be less than base
            
            # Calculate profit
            total_profit = sum(
                items_df.loc[items_df['item_id'] == item_id, 'profit_amount'].values[0]
                for item_id in cart_items['item_id']
            )
            if recommendation_accepted:
                total_profit += incremental_profit
            
            orders.append({
                'order_id': i,
                'user_id': user['user_id'],
                'user_segment': user['segment'],
                'timestamp': datetime.now() - timedelta(
                    days=np.random.randint(0, self.data_config['time_span_days'])
                ),
                'hour': hour,
                'is_peak': is_peak,
                'is_weekend': is_weekend,
                
                # Cart
                'n_items': n_items,
                'base_cart_value': round(base_cart_value, 2),
                
                # Treatment
                'recommendation_shown': recommendation_shown,
                'recommendation_accepted': recommendation_accepted,
                'propensity_score': round(propensity_score, 3),
                
                # Outcome
                'order_value': round(final_value, 2),
                'profit': round(total_profit, 2),
                'incremental_revenue': round(incremental_value if recommendation_accepted else 0, 2),
                'incremental_profit': round(incremental_profit if recommendation_accepted else 0, 2),
                
                # Ground truth (for evaluation)
                'true_treatment_effect': round(treatment_effect * 450, 2),  # True ATE
            })
        
        df = pd.DataFrame(orders)
        
        # Print causal statistics
        print(f"\n   📊 Causal Statistics:")
        treated = df[df['recommendation_shown'] == True]
        control = df[df['recommendation_shown'] == False]
        
        print(f"      Treatment group: {len(treated):,} ({len(treated)/len(df):.1%})")
        print(f"      Control group: {len(control):,} ({len(control)/len(df):.1%})")
        print(f"      Acceptance rate: {df['recommendation_accepted'].mean():.1%}")
        print(f"      Avg incremental revenue: ₹{df['incremental_revenue'].mean():.2f}")
        print(f"      Avg incremental profit: ₹{df['incremental_profit'].mean():.2f}")
        
        return df


if __name__ == "__main__":
    generator = CausalDataGenerator()
    generator.generate_all()
