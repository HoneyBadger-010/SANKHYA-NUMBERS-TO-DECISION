"""
SANKHYA Streamlit Dashboard with Folium Maps
An interactive Python-based dashboard with real-time map visualization
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium, folium_static
import json
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="SANKHYA - Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main { background-color: #f8f9fa; }
    
    h1, h2, h3, h4 { font-family: 'Poppins', sans-serif !important; }
    
    .stMetric {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
    }
    
    .stMetric label { color: rgba(255,255,255,0.9) !important; }
    .stMetric .css-1wivap2 { color: white !important; }
    
    .kpi-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        text-align: center;
    }
    
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
        color: #1a1a2e;
    }
    
    .kpi-label {
        font-size: 0.9rem;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .critical { color: #ef4444; }
    .warning { color: #f59e0b; }
    .success { color: #10b981; }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
</style>
""", unsafe_allow_html=True)

# Data paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, 'data', 'sankhya_data.json')

@st.cache_data
def load_data():
    """Load preprocessed SANKHYA data"""
    try:
        with open(DATA_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("⚠️ Data file not found. Please run generate_data.py first!")
        return None

def create_india_folium_map(data, show_centers=True, show_dsi=True, show_heatmap=False):
    """Create interactive Folium map with Aadhaar centers and DSI markers"""
    
    # Center on India
    m = folium.Map(
        location=[22.5, 82],
        zoom_start=5,
        tiles='OpenStreetMap',
        control_scale=True
    )
    
    # Add tile layers
    folium.TileLayer('cartodbpositron', name='Light Mode').add_to(m)
    folium.TileLayer('cartodbdark_matter', name='Dark Mode').add_to(m)
    
    # DSI Markers with clustering
    if show_dsi and 'map_markers' in data:
        dsi_cluster = MarkerCluster(name='DSI Districts').add_to(m)
        
        for marker in data['map_markers']:
            # Color based on DSI status
            color = '#10b981' if marker['status'] == 'low' else (
                '#f59e0b' if marker['status'] == 'medium' else '#ef4444'
            )
            
            popup_html = f"""
            <div style="font-family: 'Inter', sans-serif; min-width: 200px;">
                <h4 style="margin: 0 0 10px 0; color: #1a1a2e;">{marker['district']}</h4>
                <p style="margin: 5px 0; color: #64748b;">{marker['state']}</p>
                <hr style="margin: 10px 0; border: none; border-top: 1px solid #e2e8f0;">
                <p><strong>DSI Score:</strong> <span style="color: {color}; font-size: 1.2rem;">{marker['dsi']}</span></p>
                <p><strong>Status:</strong> <span style="text-transform: uppercase; font-weight: 600; color: {color};">{marker['status']}</span></p>
                <p><strong>Population:</strong> {marker['population']:,}</p>
                <p><strong>Capacity:</strong> {marker['capacity']} centers</p>
            </div>
            """
            
            folium.CircleMarker(
                location=[marker['lat'], marker['lng']],
                radius=8 + marker['dsi'],
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.7,
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=f"{marker['district']} | DSI: {marker['dsi']}"
            ).add_to(dsi_cluster)
    
    # Aadhaar Centers from pincode data
    if show_centers and 'aadhaar_centers' in data:
        center_cluster = MarkerCluster(name='Aadhaar Centers').add_to(m)
        
        for center in data['aadhaar_centers']:
            icon_color = 'blue' if center['center_type'] == 'PEC' else (
                'green' if center['center_type'] == 'PSK' else 'orange'
            )
            
            popup_html = f"""
            <div style="font-family: 'Inter', sans-serif; min-width: 180px;">
                <h4 style="margin: 0 0 10px 0;">📍 {center['center_type']}</h4>
                <p><strong>Pincode:</strong> {center['pincode']}</p>
                <p><strong>District:</strong> {center['district']}</p>
                <p><strong>State:</strong> {center['state']}</p>
                <hr style="margin: 8px 0; border: none; border-top: 1px solid #e2e8f0;">
                <p><strong>Transactions:</strong> {center['transactions']:,}</p>
            </div>
            """
            
            folium.Marker(
                location=[center['lat'], center['lng']],
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f"PIN: {center['pincode']} | {center['center_type']}",
                icon=folium.Icon(color=icon_color, icon='info-sign')
            ).add_to(center_cluster)
    
    # Heatmap layer
    if show_heatmap and 'map_markers' in data:
        heat_data = [[m['lat'], m['lng'], m['dsi']] for m in data['map_markers']]
        HeatMap(heat_data, name='DSI Heatmap', radius=20, blur=15).add_to(m)
    
    # Migration flow lines
    if 'migration_corridors' in data:
        migration_group = folium.FeatureGroup(name='Migration Flows')
        
        state_coords = {
            'Bihar': [25.0961, 85.3131],
            'Delhi': [28.7041, 77.1025],
            'Uttar Pradesh': [26.8467, 80.9462],
            'Maharashtra': [19.7515, 75.7139],
            'Rajasthan': [27.0238, 74.2179],
            'Gujarat': [22.2587, 71.1924],
            'Karnataka': [15.3173, 75.7139],
            'Tamil Nadu': [11.1271, 78.6569],
        }
        
        for corridor in data['migration_corridors'][:5]:
            origin = corridor.get('origin') or corridor.get('source')
            dest = corridor.get('destination')
            
            if origin in state_coords and dest in state_coords:
                folium.PolyLine(
                    locations=[state_coords[origin], state_coords[dest]],
                    weight=3,
                    color='#6366f1',
                    opacity=0.7,
                    dash_array='10',
                    popup=f"{origin} → {dest}: {corridor.get('change_percent', corridor.get('change', 0))}%"
                ).add_to(migration_group)
        
        migration_group.add_to(m)
    
    # Layer control
    folium.LayerControl().add_to(m)
    
    return m

def render_kpi_cards(kpis):
    """Render KPI cards in columns"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value">{kpis['dsi_average']}</div>
            <div class="kpi-label">Avg DSI Score</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value critical">{kpis['critical_districts']}</div>
            <div class="kpi-label">Critical Districts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value warning">{kpis['stressed_districts']}</div>
            <div class="kpi-label">Stressed Districts</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-value success">{kpis['total_districts']}</div>
            <div class="kpi-label">Total Districts</div>
        </div>
        """, unsafe_allow_html=True)

def render_stressed_districts_table(data):
    """Render stressed districts table"""
    if 'stressed_districts' not in data:
        return
    
    df = pd.DataFrame(data['stressed_districts'])
    
    # Style function for DSI colors
    def color_dsi(val):
        if val >= 6.6:
            return 'background-color: #fee2e2; color: #dc2626'
        elif val >= 3.3:
            return 'background-color: #fef3c7; color: #d97706'
        else:
            return 'background-color: #d1fae5; color: #059669'
    
    styled_df = df.style.applymap(color_dsi, subset=['dsi'])
    st.dataframe(styled_df, use_container_width=True, height=400)

def render_demand_forecast_chart(data):
    """Render demand forecast using Plotly"""
    if 'demand_forecast' not in data:
        return
    
    forecast = data['demand_forecast']
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=[f['day'] for f in forecast],
        y=[f['predicted'] for f in forecast],
        name='Predicted Demand',
        mode='lines+markers',
        line=dict(color='#6366f1', width=3),
        fill='tozeroy',
        fillcolor='rgba(99, 102, 241, 0.2)'
    ))
    
    fig.add_trace(go.Scatter(
        x=[f['day'] for f in forecast],
        y=[f['capacity'] for f in forecast],
        name='Capacity',
        mode='lines',
        line=dict(color='#10b981', width=2, dash='dash')
    ))
    
    fig.update_layout(
        title='AI Demand Forecast (Next 7 Days)',
        xaxis_title='Day',
        yaxis_title='Volume',
        template='plotly_white',
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02),
        height=350
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_anomalies_chart(data):
    """Render anomalies as a bar chart"""
    if 'anomalies' not in data or not data['anomalies']:
        st.info("No anomalies detected")
        return
    
    df = pd.DataFrame(data['anomalies'])
    
    fig = px.bar(
        df, 
        x='district', 
        y='deviation',
        color='severity',
        color_discrete_map={'critical': '#ef4444', 'warning': '#f59e0b'},
        title='Transaction Anomalies by District',
        labels={'deviation': 'Deviation %', 'district': 'District'}
    )
    
    fig.update_layout(template='plotly_white', height=350)
    st.plotly_chart(fig, use_container_width=True)

def main():
    """Main Streamlit app"""
    
    # Sidebar
    with st.sidebar:
        st.image("images/sankhya_logo.png", width=150)
        st.markdown("### *From Numbers to Decisions*")
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["🏠 Command Center", "📊 Demographics", "🗺️ Migration Radar", 
             "⚙️ Resource Lab", "🔍 System Health"]
        )
        
        st.markdown("---")
        st.markdown("### Map Settings")
        show_centers = st.checkbox("Show Aadhaar Centers", value=True)
        show_dsi = st.checkbox("Show DSI Markers", value=True)
        show_heatmap = st.checkbox("Show Heatmap", value=False)
        
        st.markdown("---")
        st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Load data
    data = load_data()
    
    if data is None:
        st.stop()
    
    # Page routing
    if page == "🏠 Command Center":
        st.title("🛡️ SANKHYA Command Center")
        st.markdown("*Predictive Governance Dashboard for UIDAI Operations*")
        
        # KPIs
        st.markdown("### Key Performance Indicators")
        render_kpi_cards(data['kpis'])
        
        st.markdown("---")
        
        # Map and Stressed Districts
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🗺️ Interactive Pulse Map")
            folium_map = create_india_folium_map(data, show_centers, show_dsi, show_heatmap)
            st_folium(folium_map, width=None, height=500)
        
        with col2:
            st.markdown("### 🚨 Top Stressed Districts")
            render_stressed_districts_table(data)
        
        st.markdown("---")
        
        # Charts row
        col1, col2 = st.columns(2)
        
        with col1:
            render_demand_forecast_chart(data)
        
        with col2:
            render_anomalies_chart(data)
    
    elif page == "📊 Demographics":
        st.title("📊 Demographic Hub")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Child Transition Gap Analysis")
            if 'child_gaps' in data and data['child_gaps']:
                df = pd.DataFrame(data['child_gaps'])
                st.dataframe(df, use_container_width=True)
        
        with col2:
            st.markdown("### Blue Zone Analysis (60+ Seniors)")
            if 'blue_zones' in data and data['blue_zones']:
                df = pd.DataFrame(data['blue_zones'])
                st.dataframe(df, use_container_width=True)
    
    elif page == "🗺️ Migration Radar":
        st.title("🗺️ Migration Radar")
        
        st.markdown("### Migration Flow Map")
        migration_map = create_india_folium_map(data, show_centers=False, show_dsi=False, show_heatmap=False)
        st_folium(migration_map, width=None, height=500)
        
        st.markdown("### Top Migration Corridors")
        if 'migration_corridors' in data:
            for corridor in data['migration_corridors'][:5]:
                origin = corridor.get('origin') or corridor.get('source')
                dest = corridor.get('destination')
                change = corridor.get('change_percent') or corridor.get('change', 0)
                volume = corridor.get('volume', 0)
                
                st.markdown(f"""
                <div style="background: white; padding: 15px; border-radius: 8px; margin: 10px 0; 
                            border-left: 4px solid {'#10b981' if change > 0 else '#ef4444'};">
                    <strong>{origin}</strong> → <strong>{dest}</strong>
                    <span style="float: right; color: {'#10b981' if change > 0 else '#ef4444'}; font-weight: 600;">
                        {'+' if change > 0 else ''}{change}%
                    </span>
                    <br><small style="color: #64748b;">{volume:,} movements</small>
                </div>
                """, unsafe_allow_html=True)
    
    elif page == "⚙️ Resource Lab":
        st.title("⚙️ Resource Lab")
        
        render_demand_forecast_chart(data)
        
        st.markdown("### Dead Centers (Low Activity)")
        if 'dead_centers' in data and data['dead_centers']:
            df = pd.DataFrame(data['dead_centers'])
            st.dataframe(df, use_container_width=True)
    
    elif page == "🔍 System Health":
        st.title("🔍 System Health Monitor")
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("System Uptime", "99.97%", "↑ 0.02%")
        col2.metric("Avg Response", "128ms", "↓ 15ms")
        col3.metric("Active Anomalies", len(data.get('anomalies', [])), "")
        col4.metric("Network Health", "98.5%", "↑ 1.2%")
        
        st.markdown("---")
        render_anomalies_chart(data)

if __name__ == "__main__":
    main()
