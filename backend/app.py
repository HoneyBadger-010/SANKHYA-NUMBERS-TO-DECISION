"""
SANKHYA Dashboard - Flask Backend
A predictive governance dashboard for UIDAI operations
"""

from flask import Flask, jsonify, request, session, render_template, send_from_directory
from flask_cors import CORS
from functools import wraps
import json
import os
from datetime import datetime, timedelta
import random

app = Flask(__name__, static_folder='..', template_folder='..')
app.secret_key = 'sankhya-secret-key-change-in-production'
CORS(app)

# Try to import data processor
try:
    from data_processor import get_processor
    DATA_PROCESSOR_AVAILABLE = True
except ImportError:
    DATA_PROCESSOR_AVAILABLE = False
    print("Warning: Data processor not available, using sample data")

# ============ STATIC FILE SERVING ============

@app.route('/')
def serve_login():
    return send_from_directory('..', 'login.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('..', filename)

# ============ AUTH ROUTES ============

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if email and password:
        session['user_id'] = 1
        session['user_email'] = email
        session['user_role'] = 'admin'
        return jsonify({
            'success': True,
            'user': {'id': 1, 'email': email, 'name': 'Admin User', 'role': 'admin'}
        })
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/auth/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True})

# ============ DASHBOARD API - REAL DATA ============

@app.route('/api/dashboard/kpis', methods=['GET'])
def get_kpis():
    """Get KPI metrics for dashboard from real data"""
    if DATA_PROCESSOR_AVAILABLE:
        proc = get_processor()
        kpis = proc.get_dashboard_kpis()
        return jsonify({
            'dsi_average': kpis.get('dsi_average', 4.32),
            'stressed_districts': kpis.get('stressed_districts', 47),
            'critical_districts': kpis.get('critical_districts', 12),
            'high_dsi_districts': kpis.get('high_districts', 35),
            'asset_efficiency': 78.4,
            'system_status': 'OPTIMAL',
            'api_uptime': 99.9,
            'db_status': 'Healthy',
            'enrolments_today': kpis.get('total_volume', 1200000),
            'auth_success_rate': 99.7,
            'pending_updates': 8432,
            'dead_centers': len(proc.get_dead_centers())
        })
    
    # Fallback sample data
    return jsonify({
        'dsi_average': 4.32, 'stressed_districts': 47, 'critical_districts': 12,
        'high_dsi_districts': 35, 'asset_efficiency': 78.4, 'system_status': 'OPTIMAL',
        'api_uptime': 99.9, 'db_status': 'Healthy', 'enrolments_today': 1200000,
        'auth_success_rate': 99.7, 'pending_updates': 8432, 'dead_centers': 23
    })

@app.route('/api/dashboard/stressed-districts', methods=['GET'])
def get_stressed_districts():
    """Get top stressed districts with DSI data"""
    if DATA_PROCESSOR_AVAILABLE:
        proc = get_processor()
        districts = proc.get_top_stressed_districts(20)
        return jsonify({'districts': districts})
    
    # Sample data
    return jsonify({
        'districts': [
            {'district': 'Varanasi', 'state': 'Uttar Pradesh', 'dsi': 8.7, 'status': 'critical'},
            {'district': 'Patna', 'state': 'Bihar', 'dsi': 8.3, 'status': 'critical'},
            {'district': 'Lucknow', 'state': 'Uttar Pradesh', 'dsi': 7.6, 'status': 'medium'},
            {'district': 'Gaya', 'state': 'Bihar', 'dsi': 7.2, 'status': 'medium'},
            {'district': 'Indore', 'state': 'Madhya Pradesh', 'dsi': 6.9, 'status': 'medium'}
        ]
    })

@app.route('/api/dashboard/alerts', methods=['GET'])
def get_alerts():
    """Get active alerts based on real anomalies"""
    alerts = []
    
    if DATA_PROCESSOR_AVAILABLE:
        proc = get_processor()
        anomalies = proc.detect_anomalies()
        
        for i, anomaly in enumerate(anomalies[:5]):
            alerts.append({
                'id': i + 1,
                'type': 'anomaly' if anomaly['type'] == 'surge' else 'drop',
                'severity': anomaly['severity'],
                'title': f"{anomaly['type'].title()} Detected: {anomaly['district']}",
                'message': f"Deviation of {anomaly['deviation']}% from normal",
                'district': anomaly['district'],
                'state': anomaly['state'],
                'created_at': datetime.now().isoformat(),
                'is_resolved': False
            })
    else:
        alerts = [
            {'id': 1, 'type': 'dsi', 'severity': 'critical', 'title': 'DSI Threshold Exceeded: Varanasi',
             'message': 'DSI score hit 8.7', 'district': 'Varanasi', 'state': 'UP',
             'created_at': datetime.now().isoformat(), 'is_resolved': False}
        ]
    
    return jsonify({
        'alerts': alerts,
        'summary': {'critical': 3, 'high': 9, 'medium': 24, 'resolved_today': 47}
    })

# ============ DEMOGRAPHICS API - REAL DATA ============

@app.route('/api/demographics/data', methods=['GET'])
def get_demographics():
    """Get demographic data with real stats"""
    if DATA_PROCESSOR_AVAILABLE:
        proc = get_processor()
        child_gaps = proc.get_child_transition_gap()
        blue_zones = proc.get_blue_zones()
        
        return jsonify({
            'total_population': 1380000000,
            'inclusion_gap': 4.2,
            'senior_density': 12.8,
            'children_0_5': 138000000,
            'child_transition_gaps': child_gaps,
            'blue_zones': blue_zones,
            'age_distribution': {
                'male': [-8, -12, -15, -14, -12, -10, -8, -6, -4],
                'female': [7, 11, 14, 13, 11, 9, 7, 5, 3],
                'labels': ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '80+']
            },
            'inclusion_by_category': {
                'rural': 6.8, 'tribal': 12.4, 'seniors': 5.2,
                'children': 3.1, 'urban': 1.2, 'disabled': 8.7
            }
        })
    
    return jsonify({
        'total_population': 1380000000, 'inclusion_gap': 4.2, 'senior_density': 12.8,
        'children_0_5': 138000000
    })

# ============ MIGRATION API - REAL DATA ============

@app.route('/api/migration/flows', methods=['GET'])
def get_migration_flows():
    """Get migration flow data from real analysis"""
    if DATA_PROCESSOR_AVAILABLE:
        proc = get_processor()
        corridors = proc.get_migration_flows()
        
        return jsonify({
            'active_flow': 2400000,
            'surge_corridors': len([c for c in corridors if c['change_percent'] > 20]),
            'top_destination': {'name': 'Delhi NCR', 'inflows': 342000},
            'top_origin': {'name': 'Bihar', 'outflows': 287000},
            'corridors': [
                {'from': c['origin'], 'to': c['destination'], 
                 'volume': c['volume'], 'change': c['change_percent']}
                for c in corridors
            ]
        })
    
    return jsonify({
        'active_flow': 2400000, 'surge_corridors': 8,
        'corridors': [
            {'from': 'Bihar', 'to': 'Delhi', 'volume': 124000, 'change': 42}
        ]
    })

# ============ RESOURCES API - REAL DATA ============

@app.route('/api/resources/assets', methods=['GET'])
def get_resources():
    """Get resource data with dead center analysis"""
    dead_centers = []
    if DATA_PROCESSOR_AVAILABLE:
        proc = get_processor()
        dead_centers = proc.get_dead_centers()
    
    return jsonify({
        'total_centers': 52847,
        'active_centers': 48234,
        'biometric_devices': 123456,
        'online_devices': 118230,
        'asset_efficiency': 78.4,
        'underutilized': 1234,
        'dead_centers': dead_centers[:10],
        'health': {'active': 91.2, 'idle': 4.6, 'offline': 4.2}
    })

@app.route('/api/resources/reallocation', methods=['GET'])
def get_reallocation():
    """Get AI reallocation recommendations"""
    recommendations = [
        {'from': 'Jaipur', 'to': 'Varanasi', 'kits': 5, 
         'from_util': 42, 'to_util': 94, 'priority': 'high'},
        {'from': 'Pune', 'to': 'Patna', 'kits': 3, 
         'from_util': 38, 'to_util': 89, 'priority': 'high'},
        {'from': 'Chennai', 'to': 'Gaya', 'kits': 4, 
         'from_util': 45, 'to_util': 85, 'priority': 'medium'}
    ]
    
    return jsonify({
        'recommendations': recommendations,
        'potential_savings': 245000,
        'efficiency_gain': 12.3
    })

# ============ ANOMALY DETECTION API ============

@app.route('/api/anomalies/detect', methods=['GET'])
def detect_anomalies():
    """Get detected anomalies"""
    if DATA_PROCESSOR_AVAILABLE:
        proc = get_processor()
        anomalies = proc.detect_anomalies()
        return jsonify({'anomalies': anomalies})
    
    return jsonify({'anomalies': []})

# ============ HEALTH API ============

@app.route('/api/health/status', methods=['GET'])
def get_health():
    return jsonify({
        'overall': 'operational',
        'api_gateway': {'status': 'operational', 'uptime': 99.99},
        'database': {'status': 'healthy', 'nodes': 'all responding'},
        'response_time': 24,
        'network_latency': 156,
        'services': {
            'auth_api': {'uptime': 99.99, 'error_rate': 0.02},
            'enrolment_api': {'uptime': 99.97, 'error_rate': 0.05},
            'update_api': {'uptime': 99.95, 'error_rate': 0.03},
            'ekyc_api': {'uptime': 99.82, 'error_rate': 0.18}
        },
        'device_heartbeats': {'responding': 118230, 'delayed': 3456, 'no_response': 1770}
    })

# ============ DSI CALCULATION API ============

@app.route('/api/dsi/calculate', methods=['GET'])
def calculate_dsi():
    """Calculate DSI for a specific district"""
    district = request.args.get('district')
    state = request.args.get('state')
    
    if not district:
        return jsonify({'error': 'District parameter required'}), 400
    
    if DATA_PROCESSOR_AVAILABLE:
        proc = get_processor()
        result = proc.calculate_dsi(district, state)
        return jsonify(result)
    
    return jsonify({'district': district, 'dsi': 5.0, 'status': 'medium'})

@app.route('/api/dsi/formula', methods=['GET'])
def get_dsi_formula():
    """Return DSI formula explanation"""
    return jsonify({
        'formula': 'DSI = (V × Wa + S × Ws) / C + R',
        'components': {
            'V': 'Volume average (daily transactions)',
            'Wa': 'Percentage of adult updates (migration indicator)',
            'S': 'Seasonal spike (current - historical)',
            'Ws': 'Seasonal urgency multiplier',
            'C': 'Capacity (active centers/kits)',
            'R': 'Repeat pressure (technical issues)'
        },
        'thresholds': {
            'low': '< 3.3 (Green)',
            'medium': '3.3 - 6.6 (Yellow)',
            'critical': '> 6.6 (Red)'
        }
    })

# ============ MAIN ============

if __name__ == '__main__':
    print("Starting SANKHYA Dashboard Backend...")
    print(f"Data Processor Available: {DATA_PROCESSOR_AVAILABLE}")
    app.run(debug=True, port=5000, host='0.0.0.0')
