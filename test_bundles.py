import sys
sys.path.insert(0, '.')
from src.models.smart_bundles import SmartBundleOptimizer
import pandas as pd

optimizer = SmartBundleOptimizer()
items = pd.read_parquet('data/raw/items.parquet')

# Test 1: Dal Makhani in cart
print('\n=== TEST 1: Dal Makhani ===')
cart1 = [{'item_id': 3, 'item_name': 'Dal Makhani', 'price': 180, 'category': 'Main Course', 'profit_margin': 0.42}]
bundles1 = optimizer.create_smart_bundles(cart1, items)
if bundles1:
    print(f'Bundle: {bundles1[0]["name"]}')
    print(f'Items: {[item["item_name"] for item in bundles1[0]["items"]]}')
    print(f'Savings: ₹{bundles1[0]["savings"]:.0f}')

# Test 2: Biryani in cart
print('\n=== TEST 2: Biryani ===')
cart2 = [{'item_id': 1, 'item_name': 'Biryani', 'price': 250, 'category': 'Main Course', 'profit_margin': 0.35}]
bundles2 = optimizer.create_smart_bundles(cart2, items)
if bundles2:
    print(f'Bundle: {bundles2[0]["name"]}')
    print(f'Items: {[item["item_name"] for item in bundles2[0]["items"]]}')
    print(f'Savings: ₹{bundles2[0]["savings"]:.0f}')

# Test 3: Paneer Tikka (Starter) in cart
print('\n=== TEST 3: Paneer Tikka ===')
cart3 = [{'item_id': 9, 'item_name': 'Paneer Tikka', 'price': 220, 'category': 'Starter', 'profit_margin': 0.38}]
bundles3 = optimizer.create_smart_bundles(cart3, items)
if bundles3:
    print(f'Bundle: {bundles3[0]["name"]}')
    print(f'Items: {[item["item_name"] for item in bundles3[0]["items"]]}')
    print(f'Savings: ₹{bundles3[0]["savings"]:.0f}')

# Test 4: Naan (Bread) in cart
print('\n=== TEST 4: Naan ===')
cart4 = [{'item_id': 15, 'item_name': 'Naan', 'price': 40, 'category': 'Bread', 'profit_margin': 0.50}]
bundles4 = optimizer.create_smart_bundles(cart4, items)
if bundles4:
    print(f'Bundle: {bundles4[0]["name"]}')
    print(f'Items: {[item["item_name"] for item in bundles4[0]["items"]]}')
    print(f'Savings: ₹{bundles4[0]["savings"]:.0f}')
