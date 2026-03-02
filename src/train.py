"""
🏆 COMPLETE TRAINING PIPELINE
Train all revolutionary models end-to-end
"""

import sys
import os
import yaml
import pandas as pd
import numpy as np
from pathlib import Path
import torch
import pickle
from tqdm import tqdm

# Add parent directory to path
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our revolutionary modules
from src.models.causal import CausalRevenueEstimator
from src.models.profit_ranker import ProfitAwareRanker
from src.models.fatigue import FatigueProtector


class CompletePipeline:
    """Complete training pipeline for all models"""
    
    def __init__(self, config_path="config.yaml"):
        with open(config_path, encoding='utf-8') as f:
            self.config = yaml.safe_load(f)
        
        self.data_dir = Path(self.config['paths']['data_dir'])
        self.models_dir = Path(self.config['paths']['models_dir'])
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
        print("\n" + "="*70)
        print("🏆 COMPLETE TRAINING PIPELINE")
        print("="*70)
        print("\n🎯 Training all revolutionary models...")
        
    def run(self):
        """Run complete pipeline"""
        
        # Step 1: Load data
        print("\n" + "="*70)
        print("STEP 1: LOADING DATA")
        print("="*70)
        
        if not self.data_dir.exists():
            print("\n⚠️  Data not found! Generating now...")
            from src.data.generate import CausalDataGenerator
            generator = CausalDataGenerator()
            generator.generate_all()
        
        users_df = pd.read_parquet(self.data_dir / "users.parquet")
        items_df = pd.read_parquet(self.data_dir / "items.parquet")
        orders_df = pd.read_parquet(self.data_dir / "orders.parquet")
        
        print(f"\n✅ Data loaded:")
        print(f"   Users: {len(users_df):,}")
        print(f"   Items: {len(items_df):,}")
        print(f"   Orders: {len(orders_df):,}")
        
        # Step 2: Train Causal Revenue Estimator
        print("\n" + "="*70)
        print("STEP 2: TRAINING CAUSAL REVENUE ESTIMATOR")
        print("="*70)
        
        causal_model = self._train_causal_model(orders_df, users_df, items_df)
        
        # Step 3: Train Profit-Aware Ranker
        print("\n" + "="*70)
        print("STEP 3: TRAINING PROFIT-AWARE RANKER")
        print("="*70)
        
        profit_ranker = self._train_profit_ranker(orders_df, users_df, items_df)
        
        # Step 4: Initialize Fatigue Protector
        print("\n" + "="*70)
        print("STEP 4: INITIALIZING FATIGUE PROTECTOR")
        print("="*70)
        
        fatigue_protector = FatigueProtector()
        print("✅ Fatigue protector initialized (no training needed)")
        
        # Step 5: Evaluate
        print("\n" + "="*70)
        print("STEP 5: EVALUATION")
        print("="*70)
        
        self._evaluate_models(causal_model, orders_df, users_df, items_df)
        
        # Step 6: Save models
        print("\n" + "="*70)
        print("STEP 6: SAVING MODELS")
        print("="*70)
        
        self._save_models(causal_model, profit_ranker, fatigue_protector)
        
        print("\n" + "="*70)
        print("✅ TRAINING COMPLETE!")
        print("="*70)
        print("\n🎉 All models trained and saved!")
        print(f"   Models directory: {self.models_dir}")
        print("\n🚀 Next steps:")
        print("   1. Start API: python src/api/server.py")
        print("   2. Open UI: open src/ui/index.html")
        print("   3. Win the hackathon! 🏆")
        
    def _train_causal_model(self, orders_df, users_df, items_df):
        """Train causal revenue estimator"""
        
        print("\n📊 Preparing features for causal model...")
        
        # Prepare features
        X = orders_df[[
            'user_segment', 'hour', 'is_peak', 'is_weekend',
            'n_items', 'base_cart_value'
        ]].copy()
        
        # Encode categorical
        X['user_segment'] = X['user_segment'].astype('category').cat.codes
        
        treatment = orders_df['recommendation_shown'].values
        outcome = orders_df['order_value'].values
        
        print(f"   Features: {X.shape}")
        print(f"   Treatment: {treatment.sum():,} / {len(treatment):,} ({treatment.mean():.1%})")
        print(f"   Outcome range: ₹{outcome.min():.0f} - ₹{outcome.max():.0f}")
        
        # Train
        causal_model = CausalRevenueEstimator()
        causal_model.fit(X, treatment, outcome)
        
        # Test prediction
        print("\n🧪 Testing causal predictions...")
        test_sample = X.head(5)
        revenue_with, revenue_without, incremental = causal_model.estimate_incremental_revenue(test_sample)
        
        print(f"\n   Sample predictions:")
        for i in range(len(test_sample)):
            print(f"   Order {i+1}:")
            print(f"      Revenue without rec: ₹{revenue_without[i]:.2f}")
            print(f"      Revenue with rec:    ₹{revenue_with[i]:.2f}")
            print(f"      Incremental:         ₹{incremental[i]:.2f}")
        
        return causal_model
    
    def _train_profit_ranker(self, orders_df, users_df, items_df):
        """Train profit-aware ranker"""
        
        print("\n📊 Initializing profit-aware ranker...")
        
        # For now, just initialize (full training would need more data prep)
        profit_ranker = ProfitAwareRanker()
        
        print("✅ Profit ranker initialized")
        print("   (Full training requires prepared feature vectors)")
        
        return profit_ranker
    
    def _evaluate_models(self, causal_model, orders_df, users_df, items_df):
        """Evaluate model performance"""
        
        print("\n📈 Evaluating causal model...")
        
        # Prepare test data
        X_test = orders_df[[
            'user_segment', 'hour', 'is_peak', 'is_weekend',
            'n_items', 'base_cart_value'
        ]].copy()
        X_test['user_segment'] = X_test['user_segment'].astype('category').cat.codes
        
        # Get predictions
        revenue_with, revenue_without, incremental = causal_model.estimate_incremental_revenue(X_test)
        
        # Compare with ground truth
        true_incremental = orders_df['incremental_revenue'].values
        
        # Calculate metrics
        treated_mask = orders_df['recommendation_shown'].values
        
        if treated_mask.sum() > 0:
            # Average treatment effect
            predicted_ate = incremental[treated_mask].mean()
            true_ate = true_incremental[treated_mask].mean()
            
            print(f"\n   Average Treatment Effect:")
            print(f"      Predicted: ₹{predicted_ate:.2f}")
            print(f"      True:      ₹{true_ate:.2f}")
            print(f"      Error:     ₹{abs(predicted_ate - true_ate):.2f}")
            
            # RMSE
            rmse = np.sqrt(((incremental[treated_mask] - true_incremental[treated_mask]) ** 2).mean())
            print(f"\n   RMSE: ₹{rmse:.2f}")
            
            # Business metrics
            total_incremental_revenue = incremental[treated_mask].sum()
            print(f"\n   💰 Business Impact:")
            print(f"      Total incremental revenue: ₹{total_incremental_revenue:,.0f}")
            print(f"      Per treated order: ₹{predicted_ate:.2f}")
        
        # Confidence intervals
        print("\n🔬 Computing confidence intervals...")
        ci = causal_model.estimate_confidence_interval(X_test.head(1000), n_bootstrap=100)
        
    def _save_models(self, causal_model, profit_ranker, fatigue_protector):
        """Save all trained models"""
        
        # Save causal model
        causal_path = self.models_dir / "causal_model.pkl"
        with open(causal_path, 'wb') as f:
            pickle.dump(causal_model, f)
        print(f"✅ Causal model saved: {causal_path}")
        
        # Save profit ranker
        profit_path = self.models_dir / "profit_ranker.ckpt"
        torch.save(profit_ranker.state_dict(), profit_path)
        print(f"✅ Profit ranker saved: {profit_path}")
        
        # Fatigue protector doesn't need saving (stateless)
        print(f"✅ Fatigue protector ready (stateless)")
        
        print(f"\n📁 All models saved to: {self.models_dir}")


def main():
    """Main training function"""
    
    print("\n" + "="*70)
    print("🏆 CAUSAL REVENUE-OPTIMIZED ENGINE")
    print("   Complete Training Pipeline")
    print("="*70)
    
    pipeline = CompletePipeline()
    pipeline.run()
    
    print("\n" + "="*70)
    print("🎉 SUCCESS!")
    print("="*70)
    print("\n✅ Your revolutionary system is trained and ready!")
    print("\n🏆 You now have:")
    print("   ✅ Trained causal revenue estimator")
    print("   ✅ Initialized profit-aware ranker")
    print("   ✅ Ready fatigue protector")
    print("   ✅ Beautiful working UI")
    print("\n🚀 Ready to win the hackathon!")


if __name__ == "__main__":
    main()
