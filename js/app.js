/**
 * SANKHYA Dashboard - Enhanced Application JavaScript
 * Real-time data integration with Flask backend
 */

// API Configuration
const API_BASE = window.location.hostname === 'localhost' ? 'http://localhost:5000/api' : '/api';

// ============ UTILITY FUNCTIONS ============

const formatNumber = (num) => {
    if (num >= 1000000000) return (num / 1000000000).toFixed(2) + 'B';
    if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
    if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
    return num.toString();
};

const formatPercent = (num) => (num || 0).toFixed(1) + '%';

const getDSIColor = (dsi) => {
    if (dsi < 3.3) return '#10b981'; // Green
    if (dsi < 6.6) return '#f59e0b'; // Yellow
    return '#ef4444'; // Red
};

const getDSIStatus = (dsi) => {
    if (dsi < 3.3) return 'low';
    if (dsi < 6.6) return 'medium';
    return 'critical';
};

// ============ API CALLS ============

async function fetchData(endpoint) {
    try {
        const response = await fetch(API_BASE + endpoint);
        if (!response.ok) throw new Error(`API Error: ${response.status}`);
        return await response.json();
    } catch (error) {
        console.warn('API fetch failed, using fallback:', error.message);
        return null;
    }
}

// ============ DASHBOARD INITIALIZATION ============

async function initDashboard() {
    console.log('🚀 SANKHYA Dashboard initializing...');

    // Load KPIs
    updateKPIs();

    // Load stressed districts if table exists
    loadStressedDistricts();

    // Initialize charts
    initPredictionChart();

    // Set up auto-refresh
    setInterval(updateKPIs, 60000);

    console.log('✅ Dashboard initialized');
}

async function updateKPIs() {
    const kpis = await fetchData('/dashboard/kpis');
    if (!kpis) return;

    // Update DSI Average
    const dsiEl = document.querySelector('[data-kpi="dsi"]');
    if (dsiEl) dsiEl.textContent = kpis.dsi_average;

    // Update Stressed Districts
    const stressedEl = document.querySelector('[data-kpi="stressed"]');
    if (stressedEl) stressedEl.textContent = kpis.stressed_districts;

    // Update Efficiency
    const efficiencyEl = document.querySelector('[data-kpi="efficiency"]');
    if (efficiencyEl) {
        efficiencyEl.textContent = formatPercent(kpis.asset_efficiency);
        const progressBar = document.querySelector('[data-kpi="efficiency-bar"]');
        if (progressBar) progressBar.style.width = kpis.asset_efficiency + '%';
    }

    // Update Dead Centers
    const deadEl = document.querySelector('[data-kpi="dead-centers"]');
    if (deadEl) deadEl.textContent = kpis.dead_centers;

    // Update Enrolments
    const enrolEl = document.querySelector('[data-kpi="enrolments"]');
    if (enrolEl) enrolEl.textContent = formatNumber(kpis.enrolments_today);
}

async function loadStressedDistricts() {
    const tableBody = document.querySelector('#stressed-districts-table tbody');
    if (!tableBody) return;

    const data = await fetchData('/dashboard/stressed-districts');
    if (!data || !data.districts) return;

    tableBody.innerHTML = data.districts.slice(0, 5).map(d => `
    <tr>
      <td>
        <div class="d-flex align-items-center">
          <span class="dsi-indicator dsi-${getDSIStatus(d.dsi)} me-2"></span>
          ${d.district}, ${d.state ? d.state.substring(0, 2).toUpperCase() : ''}
        </div>
      </td>
      <td><span class="badge bg-${d.status === 'critical' ? 'danger' : 'warning'}">${d.dsi}</span></td>
      <td class="text-${d.status === 'critical' ? 'danger' : 'warning'}">
        ${d.status === 'critical' ? '↑ +0.4' : '→ 0.0'}
      </td>
    </tr>
  `).join('');
}

// ============ PREDICTION CHART ============

function initPredictionChart() {
    const chartEl = document.getElementById('chart-prediction');
    if (!chartEl) return;

    // Check if chart already exists
    if (chartEl._chart) return;

    const chart = new ApexCharts(chartEl, {
        chart: {
            type: 'area',
            fontFamily: "'Inter', sans-serif",
            height: 250,
            toolbar: { show: false },
            animations: { enabled: true }
        },
        dataLabels: { enabled: false },
        fill: {
            opacity: 0.3,
            type: 'gradient',
            gradient: { shadeIntensity: 1, opacityFrom: 0.7, opacityTo: 0.3 }
        },
        stroke: { width: 2, curve: 'smooth' },
        series: [
            { name: 'Predicted Load', data: [42, 48, 52, 58, 55, 60, 65] },
            { name: 'Actual Load', data: [40, 45, 50, 55, 52, null, null] }
        ],
        tooltip: { theme: 'dark' },
        grid: { borderColor: 'rgba(255,255,255,0.1)', strokeDashArray: 4 },
        xaxis: {
            labels: { style: { colors: '#fff' } },
            categories: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            axisBorder: { show: false }
        },
        yaxis: {
            labels: {
                style: { colors: '#fff' },
                formatter: val => val + 'K'
            }
        },
        colors: ['#4dabf7', '#51cf66'],
        legend: { labels: { colors: '#fff' } }
    });

    chart.render();
    chartEl._chart = chart;
}

// ============ MIGRATION RADAR ============

async function loadMigrationData() {
    const data = await fetchData('/migration/flows');
    if (!data) return;

    // Update KPIs
    const activeFlowEl = document.querySelector('[data-kpi="active-flow"]');
    if (activeFlowEl) activeFlowEl.textContent = formatNumber(data.active_flow);

    // Update corridors table
    const corridorsList = document.querySelector('#migration-corridors');
    if (corridorsList && data.corridors) {
        corridorsList.innerHTML = data.corridors.map(c => `
      <div class="list-group-item">
        <div class="d-flex justify-content-between align-items-center">
          <div>
            <strong>${c.from} → ${c.to}</strong>
            <div class="text-secondary small">${formatNumber(c.volume)} monthly</div>
          </div>
          <span class="badge bg-${c.change > 20 ? 'danger' : c.change > 10 ? 'warning' : 'success'}">
            +${c.change}%
          </span>
        </div>
      </div>
    `).join('');
    }
}

// ============ RESOURCE LAB ============

async function loadResourceData() {
    const data = await fetchData('/resources/assets');
    if (!data) return;

    // Update stats
    document.querySelectorAll('[data-kpi="total-centers"]').forEach(el => {
        el.textContent = formatNumber(data.total_centers);
    });

    document.querySelectorAll('[data-kpi="biometric-devices"]').forEach(el => {
        el.textContent = formatNumber(data.biometric_devices);
    });

    // Load reallocation recommendations
    loadReallocationRecommendations();
}

async function loadReallocationRecommendations() {
    const data = await fetchData('/resources/reallocation');
    if (!data) return;

    const list = document.querySelector('#reallocation-list');
    if (list && data.recommendations) {
        list.innerHTML = data.recommendations.map(r => `
      <div class="list-group-item d-flex justify-content-between align-items-center">
        <div>
          <strong>Move ${r.kits} kits: ${r.from} → ${r.to}</strong>
          <div class="text-secondary small">
            ${r.from_util}% → ${r.to_util}% utilization
          </div>
        </div>
        <div>
          <button class="btn btn-sm btn-success" onclick="acceptReallocation(${r.kits}, '${r.from}', '${r.to}')">
            Accept
          </button>
        </div>
      </div>
    `).join('');
    }
}

function acceptReallocation(kits, from, to) {
    console.log(`Accepting reallocation: ${kits} kits from ${from} to ${to}`);
    alert(`Reallocation request submitted: ${kits} kits from ${from} to ${to}`);
}

// ============ DEMOGRAPHICS ============

async function loadDemographicsData() {
    const data = await fetchData('/demographics/data');
    if (!data) return;

    // Update child gap analysis
    if (data.child_transition_gaps) {
        const gapList = document.querySelector('#child-gap-list');
        if (gapList) {
            gapList.innerHTML = data.child_transition_gaps.slice(0, 5).map(g => `
        <div class="list-group-item d-flex justify-content-between">
          <span>${g.district}, ${g.state}</span>
          <span class="badge bg-warning">${g.gap_percent.toFixed(1)}% gap</span>
        </div>
      `).join('');
        }
    }

    // Update blue zones
    if (data.blue_zones) {
        const blueList = document.querySelector('#blue-zones-list');
        if (blueList) {
            blueList.innerHTML = data.blue_zones.slice(0, 5).map(z => `
        <div class="list-group-item d-flex justify-content-between">
          <span>${z.district}, ${z.state}</span>
          <span class="badge bg-info">${formatNumber(z.senior_count)} seniors</span>
        </div>
      `).join('');
        }
    }
}

// ============ ANOMALY DETECTION ============

async function loadAnomalies() {
    const data = await fetchData('/anomalies/detect');
    if (!data || !data.anomalies) return;

    const list = document.querySelector('#anomaly-list');
    if (list) {
        list.innerHTML = data.anomalies.slice(0, 5).map(a => `
      <div class="list-group-item">
        <div class="d-flex align-items-center">
          <span class="status-dot ${a.severity === 'critical' ? 'status-dot-animated' : ''} bg-${a.severity === 'critical' ? 'danger' : 'warning'} d-block me-2"></span>
          <div>
            <strong>${a.type === 'surge' ? '↑' : '↓'} ${a.district}</strong>
            <div class="text-secondary small">${a.deviation}% deviation</div>
          </div>
        </div>
      </div>
    `).join('');
    }
}

// ============ DSI CALCULATOR ============

async function calculateDSI(district, state = null) {
    let url = `/dsi/calculate?district=${encodeURIComponent(district)}`;
    if (state) url += `&state=${encodeURIComponent(state)}`;

    const result = await fetchData(url);
    return result;
}

// ============ THEME TOGGLE ============

function toggleTheme() {
    const html = document.documentElement;
    const currentTheme = html.getAttribute('data-bs-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    html.setAttribute('data-bs-theme', newTheme);
    localStorage.setItem('theme', newTheme);
}

function loadTheme() {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-bs-theme', savedTheme);
    }
}

// ============ PAGE INITIALIZATION ============

document.addEventListener('DOMContentLoaded', function () {
    loadTheme();

    // Initialize tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipTriggerList.forEach(el => new bootstrap.Tooltip(el));

    // Determine which page we're on and initialize accordingly
    const path = window.location.pathname;

    if (path.includes('index.html') || path === '/' || path === '') {
        initDashboard();
    } else if (path.includes('migration-radar')) {
        loadMigrationData();
    } else if (path.includes('resource-lab')) {
        loadResourceData();
    } else if (path.includes('demographic-hub')) {
        loadDemographicsData();
    } else if (path.includes('system-health')) {
        loadAnomalies();
    }
});

// ============ EXPORTS ============

window.SANKHYA = {
    fetchData,
    calculateDSI,
    toggleTheme,
    formatNumber,
    getDSIColor,
    initDashboard,
    loadMigrationData,
    loadResourceData,
    loadDemographicsData,
    loadAnomalies
};

console.log('🔷 SANKHYA Application loaded');
