"""
Generate realistic food delivery data with actual menu items
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import yaml
from pathlib import Path


def generate_real_menu_data():
    """Generate data with real menu items matching the UI"""
    
    print("\n" + "="*70)
    print("🍽️  GENERATING REAL MENU DATA")
    print("="*70)
    
    # Load config
    with open("config.yaml", encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    output_dir = Path(config['paths']['data_dir'])
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Real menu items (matching UI exactly)
    items_data = [
        # Main Courses
        {'item_id': 1, 'item_name': 'Biryani', 'price': 250, 'profit_margin': 0.35, 'category': 'Main Course'},
        {'item_id': 2, 'item_name': 'Butter Chicken', 'price': 280, 'profit_margin': 0.40, 'category': 'Main Course'},
        {'item_id': 3, 'item_name': 'Dal Makhani', 'price': 180, 'profit_margin': 0.42, 'category': 'Main Course'},
        {'item_id': 4, 'item_name': 'Kadai Paneer', 'price': 240, 'profit_margin': 0.38, 'category': 'Main Course'},
        {'item_id': 5, 'item_name': 'Chicken Tikka Masala', 'price': 290, 'profit_margin': 0.39, 'category': 'Main Course'},
        {'item_id': 6, 'item_name': 'Palak Paneer', 'price': 220, 'profit_margin': 0.40, 'category': 'Main Course'},
        {'item_id': 7, 'item_name': 'Mutton Rogan Josh', 'price': 350, 'profit_margin': 0.36, 'category': 'Main Course'},
        {'item_id': 8, 'item_name': 'Veg Korma', 'price': 200, 'profit_margin': 0.43, 'category': 'Main Course'},
        
        # Starters
        {'item_id': 9, 'item_name': 'Paneer Tikka', 'price': 220, 'profit_margin': 0.38, 'category': 'Starter'},
        {'item_id': 10, 'item_name': 'Chicken 65', 'price': 240, 'profit_margin': 0.37, 'category': 'Starter'},
        {'item_id': 11, 'item_name': 'Veg Spring Rolls', 'price': 150, 'profit_margin': 0.45, 'category': 'Starter'},
        {'item_id': 12, 'item_name': 'Fish Tikka', 'price': 280, 'profit_margin': 0.35, 'category': 'Starter'},
        {'item_id': 13, 'item_name': 'Hara Bhara Kabab', 'price': 180, 'profit_margin': 0.42, 'category': 'Starter'},
        {'item_id': 14, 'item_name': 'Tandoori Chicken', 'price': 260, 'profit_margin': 0.38, 'category': 'Starter'},
        
        # Breads
        {'item_id': 15, 'item_name': 'Naan', 'price': 40, 'profit_margin': 0.50, 'category': 'Bread'},
        {'item_id': 16, 'item_name': 'Butter Naan', 'price': 50, 'profit_margin': 0.48, 'category': 'Bread'},
        {'item_id': 17, 'item_name': 'Garlic Naan', 'price': 60, 'profit_margin': 0.47, 'category': 'Bread'},
        {'item_id': 18, 'item_name': 'Roti', 'price': 30, 'profit_margin': 0.52, 'category': 'Bread'},
        {'item_id': 19, 'item_name': 'Paratha', 'price': 50, 'profit_margin': 0.49, 'category': 'Bread'},
        {'item_id': 20, 'item_name': 'Kulcha', 'price': 55, 'profit_margin': 0.48, 'category': 'Bread'},
        
        # Sides
        {'item_id': 21, 'item_name': 'Raita', 'price': 60, 'profit_margin': 0.55, 'category': 'Side'},
        {'item_id': 22, 'item_name': 'Masala Papad', 'price': 50, 'profit_margin': 0.60, 'category': 'Side'},
        {'item_id': 23, 'item_name': 'Green Salad', 'price': 80, 'profit_margin': 0.58, 'category': 'Side'},
        {'item_id': 24, 'item_name': 'Pickle', 'price': 30, 'profit_margin': 0.65, 'category': 'Side'},
        {'item_id': 25, 'item_name': 'Onion Salad', 'price': 40, 'profit_margin': 0.62, 'category': 'Side'},
        
        # Beverages
        {'item_id': 26, 'item_name': 'Lassi', 'price': 70, 'profit_margin': 0.52, 'category': 'Beverage'},
        {'item_id': 27, 'item_name': 'Mango Lassi', 'price': 90, 'profit_margin': 0.50, 'category': 'Beverage'},
        {'item_id': 28, 'item_name': 'Masala Chai', 'price': 40, 'profit_margin': 0.60, 'category': 'Beverage'},
        {'item_id': 29, 'item_name': 'Cold Coffee', 'price': 80, 'profit_margin': 0.54, 'category': 'Beverage'},
        {'item_id': 30, 'item_name': 'Fresh Lime Soda', 'price': 60, 'profit_margin': 0.58, 'category': 'Beverage'},
        
        # Desserts
        {'item_id': 31, 'item_name': 'Gulab Jamun', 'price': 80, 'profit_margin': 0.48, 'category': 'Dessert'},
        {'item_id': 32, 'item_name': 'Rasmalai', 'price': 100, 'profit_margin': 0.46, 'category': 'Dessert'},
        {'item_id': 33, 'item_name': 'Kulfi', 'price': 70, 'profit_margin': 0.50, 'category': 'Dessert'},
        {'item_id': 34, 'item_name': 'Gajar Halwa', 'price': 90, 'profit_margin': 0.47, 'category': 'Dessert'},
        {'item_id': 35, 'item_name': 'Ice Cream', 'price': 60, 'profit_margin': 0.52, 'category': 'Dessert'},
        
        # Rice
        {'item_id': 36, 'item_name': 'Jeera Rice', 'price': 120, 'profit_margin': 0.45, 'category': 'Rice'},
        {'item_id': 37, 'item_name': 'Veg Pulao', 'price': 150, 'profit_margin': 0.43, 'category': 'Rice'},
        {'item_id': 38, 'item_name': 'Plain Rice', 'price': 100, 'profit_margin': 0.48, 'category': 'Rice'},
        {'item_id': 39, 'item_name': 'Curd Rice', 'price': 110, 'profit_margin': 0.46, 'category': 'Rice'},
        {'item_id': 40, 'item_name': 'Lemon Rice', 'price': 130, 'profit_margin': 0.44, 'category': 'Rice'}
    ]
    
    items_df = pd.DataFrame(items_data)
    
    # Generate users
    print("\n👥 Generating users...")
    n_users = 5000
    users_data = []
    
    for i in range(n_users):
        segment = np.random.choice(['budget', 'regular', 'premium', 'vip'], p=[0.3, 0.4, 0.2, 0.1])
        users_data.append({
            'user_id': i,
            'user_segment': segment,
            'order_frequency': np.random.poisson(5) + 1
        })
    
    users_df = pd.DataFrame(users_data)
    
    # Generate orders with causal structure
    print("\n📦 Generating orders with causal structure...")
    n_orders = 10000
    orders_data = []
    
    for i in range(n_orders):
        user = users_df.sample(1).iloc[0]
        
        # Select 1-5 items
        n_items = np.random.randint(1, 6)
        order_items = items_df.sample(n_items)
        
        base_cart_value = order_items['price'].sum()
        
        # Recommendation shown (treatment)
        recommendation_shown = np.random.random() < 0.5
        
        # Causal effect: recommendations increase order value
        if recommendation_shown:
            incremental_revenue = np.random.uniform(30, 100)
            order_value = base_cart_value + incremental_revenue
        else:
            incremental_revenue = 0
            order_value = base_cart_value
        
        orders_data.append({
            'order_id': i,
            'user_id': user['user_id'],
            'user_segment': user['user_segment'],
            'n_items': n_items,
            'base_cart_value': base_cart_value,
            'order_value': order_value,
            'recommendation_shown': recommendation_shown,
            'incremental_revenue': incremental_revenue,
            'hour': np.random.randint(0, 24),
            'is_peak': np.random.random() < 0.3,
            'is_weekend': np.random.random() < 0.3
        })
    
    orders_df = pd.DataFrame(orders_data)
    
    # Generate restaurants
    print("\n🏪 Generating restaurants...")
    restaurants_data = []
    for i in range(100):
        restaurants_data.append({
            'restaurant_id': i,
            'restaurant_name': f'Restaurant {i}',
            'cuisine': np.random.choice(['North Indian', 'South Indian', 'Chinese', 'Italian'])
        })
    
    restaurants_df = pd.DataFrame(restaurants_data)
    
    # Save all data
    print("\n💾 Saving data...")
    items_df.to_parquet(output_dir / "items.parquet")
    users_df.to_parquet(output_dir / "users.parquet")
    orders_df.to_parquet(output_dir / "orders.parquet")
    restaurants_df.to_parquet(output_dir / "restaurants.parquet")
    
    print("\n✅ Real menu data generated!")
    print(f"\n📊 Statistics:")
    print(f"   Items: {len(items_df)} (real menu items)")
    print(f"   Users: {len(users_df):,}")
    print(f"   Orders: {len(orders_df):,}")
    print(f"   Restaurants: {len(restaurants_df)}")
    
    print(f"\n🍽️  Menu Categories:")
    for cat, count in items_df['category'].value_counts().items():
        print(f"   {cat}: {count} items")
    
    print(f"\n💰 Average Order Value: ₹{orders_df['order_value'].mean():.2f}")
    print(f"   With Recommendations: ₹{orders_df[orders_df['recommendation_shown']]['order_value'].mean():.2f}")
    print(f"   Without Recommendations: ₹{orders_df[~orders_df['recommendation_shown']]['order_value'].mean():.2f}")
    
    return items_df, users_df, orders_df, restaurants_df


if __name__ == "__main__":
    generate_real_menu_data()
