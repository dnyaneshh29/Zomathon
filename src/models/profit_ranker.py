"""
🏆 REVOLUTIONARY: Profit-Aware Ranker
Optimizes PROFIT, not just revenue!
"""

import numpy as np
import torch
import torch.nn as nn
import pytorch_lightning as pl
from typing import Dict, List
import yaml


class ProfitAwareRanker(pl.LightningModule):
    """
    Ranks recommendations by expected PROFIT
    
    Key Innovation:
    - Traditional: rank_by(predicted_revenue)
    - Our System: rank_by(predicted_revenue × profit_margin - costs)
    
    Multi-objective optimization:
    1. Revenue (how much user will spend)
    2. Margin (how much we keep)
    3. User Satisfaction (long-term value)
    """
    
    def __init__(self, config_path="config.yaml"):
        super().__init__()
        
        with open(config_path, encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        self.profit_config = config['profit']
        self.training_config = config['training']
        
        print("\n" + "="*70)
        print("🏆 PROFIT-AWARE RANKER")
        print("="*70)
        print("\n💰 Revolutionary Feature: Profit Optimization")
        print(f"   Optimize: {self.profit_config['optimize_metric']}")
        print(f"   Revenue Weight: {self.profit_config['revenue_weight']:.1%}")
        print(f"   Margin Weight: {self.profit_config['margin_weight']:.1%}")
        print(f"   Satisfaction Weight: {self.profit_config['user_satisfaction_weight']:.1%}")
        
        # Network architecture
        self.embedding_dim = 256
        
        # User encoder
        self.user_encoder = nn.Sequential(
            nn.Linear(20, 128),  # User features
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, self.embedding_dim)
        )
        
        # Item encoder
        self.item_encoder = nn.Sequential(
            nn.Linear(15, 128),  # Item features
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, self.embedding_dim)
        )
        
        # Context encoder
        self.context_encoder = nn.Sequential(
            nn.Linear(10, 64),  # Context features
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Linear(64, 128)
        )
        
        # Multi-objective heads
        self.revenue_head = nn.Sequential(
            nn.Linear(self.embedding_dim * 2 + 128, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 1)
        )
        
        self.margin_head = nn.Sequential(
            nn.Linear(self.embedding_dim * 2 + 128, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
            nn.Sigmoid()  # Margin is between 0 and 1
        )
        
        self.satisfaction_head = nn.Sequential(
            nn.Linear(self.embedding_dim * 2 + 128, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
            nn.Sigmoid()  # Satisfaction score 0-1
        )
        
        # Acceptance probability head
        self.acceptance_head = nn.Sequential(
            nn.Linear(self.embedding_dim * 2 + 128, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 1),
            nn.Sigmoid()
        )
        
        # Loss weights
        self.revenue_weight = self.profit_config['revenue_weight']
        self.margin_weight = self.profit_config['margin_weight']
        self.satisfaction_weight = self.profit_config['user_satisfaction_weight']
        
    def forward(self, user_features, item_features, context_features):
        """
        Forward pass
        
        Returns:
            - predicted_revenue
            - predicted_margin
            - predicted_satisfaction
            - acceptance_probability
            - profit_score (combined)
        """
        
        # Encode
        user_emb = self.user_encoder(user_features)
        item_emb = self.item_encoder(item_features)
        context_emb = self.context_encoder(context_features)
        
        # Combine
        combined = torch.cat([user_emb, item_emb, context_emb], dim=1)
        
        # Predict
        revenue = self.revenue_head(combined)
        margin = self.margin_head(combined)
        satisfaction = self.satisfaction_head(combined)
        acceptance = self.acceptance_head(combined)
        
        # Profit score (UNIQUE!)
        # Expected profit = P(accept) × (revenue × margin - cost)
        cost = self.profit_config['cost_per_recommendation']
        profit_score = acceptance * (revenue * margin - cost)
        
        # Add satisfaction bonus (long-term value)
        profit_score = profit_score * (1 + 0.1 * satisfaction)
        
        return {
            'revenue': revenue,
            'margin': margin,
            'satisfaction': satisfaction,
            'acceptance': acceptance,
            'profit_score': profit_score
        }
    
    def training_step(self, batch, batch_idx):
        """Training step with multi-objective loss"""
        
        # Forward pass
        outputs = self(
            batch['user_features'],
            batch['item_features'],
            batch['context_features']
        )
        
        # Multi-objective loss
        revenue_loss = nn.functional.mse_loss(
            outputs['revenue'].squeeze(),
            batch['actual_revenue']
        )
        
        margin_loss = nn.functional.mse_loss(
            outputs['margin'].squeeze(),
            batch['actual_margin']
        )
        
        satisfaction_loss = nn.functional.mse_loss(
            outputs['satisfaction'].squeeze(),
            batch['satisfaction_score']
        )
        
        acceptance_loss = nn.functional.binary_cross_entropy(
            outputs['acceptance'].squeeze(),
            batch['was_accepted'].float()
        )
        
        # Combined loss
        loss = (
            self.revenue_weight * revenue_loss +
            self.margin_weight * margin_loss +
            self.satisfaction_weight * satisfaction_loss +
            0.3 * acceptance_loss
        )
        
        # Metrics
        self.log('train_loss', loss)
        self.log('revenue_loss', revenue_loss)
        self.log('margin_loss', margin_loss)
        self.log('satisfaction_loss', satisfaction_loss)
        
        return loss
    
    def validation_step(self, batch, batch_idx):
        """Validation step"""
        
        outputs = self(
            batch['user_features'],
            batch['item_features'],
            batch['context_features']
        )
        
        # Calculate losses
        revenue_loss = nn.functional.mse_loss(
            outputs['revenue'].squeeze(),
            batch['actual_revenue']
        )
        
        margin_loss = nn.functional.mse_loss(
            outputs['margin'].squeeze(),
            batch['actual_margin']
        )
        
        loss = self.revenue_weight * revenue_loss + self.margin_weight * margin_loss
        
        self.log('val_loss', loss)
        
        return loss
    
    def configure_optimizers(self):
        """Configure optimizer"""
        optimizer = torch.optim.AdamW(
            self.parameters(),
            lr=self.training_config['learning_rate'],
            weight_decay=0.01
        )
        
        scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
            optimizer,
            mode='min',
            factor=0.5,
            patience=3
        )
        
        return {
            'optimizer': optimizer,
            'lr_scheduler': {
                'scheduler': scheduler,
                'monitor': 'val_loss'
            }
        }
    
    def rank_candidates(
        self,
        candidates: List[Dict],
        user_features: Dict,
        context_features: Dict
    ) -> List[Dict]:
        """
        Rank candidates by expected profit
        
        Args:
            candidates: List of candidate items
            user_features: User features
            context_features: Context features
        
        Returns:
            Ranked list with profit scores
        """
        
        self.eval()
        
        results = []
        
        with torch.no_grad():
            for candidate in candidates:
                # Prepare features
                user_tensor = torch.FloatTensor([list(user_features.values())])
                item_tensor = torch.FloatTensor([list(candidate['features'].values())])
                context_tensor = torch.FloatTensor([list(context_features.values())])
                
                # Predict
                outputs = self(user_tensor, item_tensor, context_tensor)
                
                # Add scores to candidate
                candidate['predicted_revenue'] = float(outputs['revenue'][0])
                candidate['predicted_margin'] = float(outputs['margin'][0])
                candidate['predicted_satisfaction'] = float(outputs['satisfaction'][0])
                candidate['acceptance_probability'] = float(outputs['acceptance'][0])
                candidate['profit_score'] = float(outputs['profit_score'][0])
                
                # Calculate expected profit
                expected_profit = (
                    candidate['acceptance_probability'] *
                    candidate['predicted_revenue'] *
                    candidate['predicted_margin']
                )
                candidate['expected_profit'] = expected_profit
                
                results.append(candidate)
        
        # Sort by profit score (descending)
        results.sort(key=lambda x: x['profit_score'], reverse=True)
        
        return results


if __name__ == "__main__":
    print("🏆 Profit-Aware Ranker - Revolutionary Module")
    print("   First system to optimize PROFIT, not just revenue!")
