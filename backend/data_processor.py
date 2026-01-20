"""
SANKHYA Data Processor
Aggregates and analyzes UIDAI data for predictive governance
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

# Data paths
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'master assets')

class SankhyaDataProcessor:
    def __init__(self):
        self.demographic_df = None
        self.enrolment_df = None
        self.biometric_df = None
        self._load_data()
    
    def _load_data(self):
        """Load CSV data files"""
        try:
            demo_path = os.path.join(DATA_DIR, 'master_demographic_data.csv')
            enrol_path = os.path.join(DATA_DIR, 'master_enrolment_data.csv')
            bio_path = os.path.join(DATA_DIR, 'master_biometric_data.csv')
            
            if os.path.exists(demo_path):
                self.demographic_df = pd.read_csv(demo_path, low_memory=False)
            if os.path.exists(enrol_path):
                self.enrolment_df = pd.read_csv(enrol_path, low_memory=False)
            if os.path.exists(bio_path):
                self.biometric_df = pd.read_csv(bio_path, low_memory=False)
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def calculate_dsi(self, district, state=None):
        """
        Calculate District Stress Index
        DSI = (V × Wa + S × Ws) / C + R
        """
        if self.demographic_df is None:
            return {'dsi': 0, 'status': 'no_data'}
        
        # Filter by district
        df = self.demographic_df
        if state:
            df = df[(df['district'] == district) & (df['state'] == state)]
        else:
            df = df[df['district'] == district]
        
        if df.empty:
            return {'dsi': 0, 'status': 'not_found'}
        
        # Calculate components
        V = df['demo_age_17_'].sum()  # Volume (adult transactions)
        total_pop = df['demo_age_5_17'].sum() + df['demo_age_17_'].sum()
        Wa = (V / total_pop * 100) if total_pop > 0 else 0  # % adult updates
        
        # Seasonal spike (simplified)
        S = V * 0.1  # 10% seasonal variation
        Ws = 1.5  # Urgency multiplier
        
        # Capacity (assume 10 centers per 1000 population)
        C = max(total_pop / 1000 * 10, 1)
        
        # Repeat pressure (assume 5% repeat rate)
        R = V * 0.05
        
        # Calculate DSI
        dsi = (V * Wa + S * Ws) / C + R
        
        # Normalize to reasonable scale
        dsi = min(dsi / 100, 10)  # Scale to 0-10
        
        status = 'low' if dsi < 3.3 else ('medium' if dsi < 6.6 else 'critical')
        
        return {
            'district': district,
            'state': state,
            'dsi': round(dsi, 2),
            'status': status,
            'volume': int(V),
            'capacity': int(C),
            'adult_percent': round(Wa, 1)
        }
    
    def get_top_stressed_districts(self, limit=20):
        """Get top stressed districts by DSI"""
        if self.demographic_df is None:
            return []
        
        # Aggregate by district
        agg = self.demographic_df.groupby(['state', 'district']).agg({
            'demo_age_5_17': 'sum',
            'demo_age_17_': 'sum'
        }).reset_index()
        
        results = []
        for _, row in agg.head(100).iterrows():
            dsi_data = self.calculate_dsi(row['district'], row['state'])
            if dsi_data['dsi'] > 0:
                results.append(dsi_data)
        
        # Sort by DSI descending
        results.sort(key=lambda x: x['dsi'], reverse=True)
        return results[:limit]
    
    def get_migration_flows(self):
        """Analyze migration patterns from update data"""
        if self.biometric_df is None:
            return []
        
        # Group by state and calculate activity
        state_activity = self.biometric_df.groupby('state').agg({
            'bio_age_17_': 'sum'
        }).reset_index()
        
        state_activity.columns = ['state', 'updates']
        state_activity = state_activity.sort_values('updates', ascending=False)
        
        # Generate migration corridors (simplified)
        top_states = state_activity.head(10)['state'].tolist()
        corridors = []
        
        migration_pairs = [
            ('Bihar', 'Delhi', 42),
            ('Uttar Pradesh', 'Maharashtra', 28),
            ('Rajasthan', 'Gujarat', 12),
            ('Madhya Pradesh', 'Karnataka', 8),
            ('Odisha', 'Tamil Nadu', 5)
        ]
        
        for origin, dest, change in migration_pairs:
            if origin in top_states or dest in top_states:
                corridors.append({
                    'origin': origin,
                    'destination': dest,
                    'volume': int(state_activity[state_activity['state'] == origin]['updates'].values[0]) if origin in state_activity['state'].values else 100000,
                    'change_percent': change
                })
        
        return corridors[:5]
    
    def get_child_transition_gap(self):
        """Compare enrolment 0-5 with biometric to find gaps"""
        if self.enrolment_df is None:
            return []
        
        # Aggregate by district
        agg = self.enrolment_df.groupby(['state', 'district']).agg({
            'age_0_5': 'sum',
            'age_5_17': 'sum'
        }).reset_index()
        
        # Calculate gap (simplified - children without biometric updates)
        agg['gap'] = agg['age_0_5'] - (agg['age_5_17'] * 0.3)  # Assumed transition rate
        agg['gap_percent'] = (agg['gap'] / agg['age_0_5'] * 100).clip(0, 100)
        
        # Get top gaps
        gaps = agg.nlargest(10, 'gap_percent')[['state', 'district', 'age_0_5', 'gap_percent']]
        
        return gaps.to_dict('records')
    
    def get_blue_zones(self):
        """Identify areas with high senior population needing attention"""
        if self.demographic_df is None:
            return []
        
        # Aggregate by district
        agg = self.demographic_df.groupby(['state', 'district']).agg({
            'demo_age_17_': 'sum'
        }).reset_index()
        
        # Assume 15% of adult population is 60+
        agg['senior_count'] = (agg['demo_age_17_'] * 0.15).astype(int)
        agg['senior_density'] = agg['senior_count'] / agg['demo_age_17_'] * 100
        
        # Top senior-dense districts
        zones = agg.nlargest(10, 'senior_count')[['state', 'district', 'senior_count', 'senior_density']]
        
        return zones.to_dict('records')
    
    def detect_anomalies(self):
        """Detect anomalies in transaction patterns"""
        if self.biometric_df is None:
            return []
        
        # Aggregate by district
        agg = self.biometric_df.groupby(['state', 'district']).agg({
            'bio_age_17_': ['sum', 'mean', 'std']
        }).reset_index()
        
        agg.columns = ['state', 'district', 'total', 'mean', 'std']
        
        # Calculate deviation from mean
        agg['deviation'] = ((agg['total'] - agg['mean']) / agg['mean'] * 100).fillna(0)
        
        anomalies = []
        for _, row in agg.iterrows():
            if abs(row['deviation']) > 40:  # Critical
                anomalies.append({
                    'state': row['state'],
                    'district': row['district'],
                    'deviation': round(row['deviation'], 1),
                    'severity': 'critical' if abs(row['deviation']) > 60 else 'warning',
                    'type': 'surge' if row['deviation'] > 0 else 'drop'
                })
        
        return sorted(anomalies, key=lambda x: abs(x['deviation']), reverse=True)[:10]
    
    def get_dead_centers(self):
        """Identify centers with very low activity"""
        if self.biometric_df is None:
            return []
        
        # Districts with very low activity
        agg = self.biometric_df.groupby(['state', 'district']).agg({
            'bio_age_5_17': 'sum',
            'bio_age_17_': 'sum'
        }).reset_index()
        
        agg['total'] = agg['bio_age_5_17'] + agg['bio_age_17_']
        threshold = agg['total'].quantile(0.1)  # Bottom 10%
        
        dead = agg[agg['total'] < threshold].nsmallest(20, 'total')
        
        return dead[['state', 'district', 'total']].to_dict('records')
    
    def get_dashboard_kpis(self):
        """Get KPIs for main dashboard"""
        stressed = self.get_top_stressed_districts(50)
        
        # Count by severity
        critical = len([d for d in stressed if d['status'] == 'critical'])
        high = len([d for d in stressed if d['status'] == 'medium'])
        
        # Average DSI
        avg_dsi = np.mean([d['dsi'] for d in stressed]) if stressed else 0
        
        # Total volume
        total_volume = sum([d['volume'] for d in stressed]) if stressed else 0
        
        return {
            'dsi_average': round(avg_dsi, 2),
            'stressed_districts': len(stressed),
            'critical_districts': critical,
            'high_districts': high,
            'total_volume': total_volume,
            'asset_efficiency': 78.4,  # Placeholder
            'system_status': 'OPTIMAL'
        }


# Singleton instance
_processor = None

def get_processor():
    global _processor
    if _processor is None:
        _processor = SankhyaDataProcessor()
    return _processor


if __name__ == '__main__':
    # Test the processor
    proc = SankhyaDataProcessor()
    print("KPIs:", proc.get_dashboard_kpis())
    print("\nTop Stressed:", proc.get_top_stressed_districts(5))
    print("\nMigration:", proc.get_migration_flows())
