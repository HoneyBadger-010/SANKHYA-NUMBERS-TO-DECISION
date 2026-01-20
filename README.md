# SANKHYA-NUMBERS-TO-DECISION
SANKHYA - Predictive Governance Dashboard for UIDAI. Analyzes 5M+ Aadhaar records using AI to forecast demand, identify stressed districts, and optimize center resources. Features interactive India map, DSI scoring , and Blue Zone/DEZ detection. Built with Flask, Leaflet.js &amp; real-time analytics.
# SANKHYA (संख्या) - Predictive Governance Dashboard

![SANKHYA Logo](images/sankhya_logo.png)

> *"From Numbers to Decisions"*

A next-generation predictive analytics dashboard for UIDAI's Aadhaar ecosystem, analyzing 5M+ records to forecast demand, identify stressed districts, and optimize resource allocation.

---

## 🚀 Quick Start

```bash
# Navigate to backend
cd sankhya/backend

# Install dependencies
pip install -r requirements.txt

# Generate data & AI forecast
python generate_data.py
python ai_forecaster.py

# Run server
python app.py
```

**Access**: http://localhost:5000/login.html

---

## 📊 Features

### Core Analytics
| Feature | Description |
|---------|-------------|
| **DSI Scoring** | Demand Stress Index (0-10 scale) for each district |
| **7-Day AI Forecast** | ML-based demand prediction with confidence bands |
| **Blue Zone Detection** | High senior population areas requiring attention |
| **DEZ Identification** | Digital Exclusion Zones with low activity |

### Interactive Map
- 1,000+ district markers with DSI coloring
- 300+ Aadhaar center locations
- Zoom-responsive dot sizing
- Filters: Pincode, State, District, Zone
- View modes: Normal, State Avg, District Avg

### Dashboard Pages
1. **Command Center** - KPIs, Map, Forecasts
2. **Demographic Hub** - Population analytics
3. **Migration Radar** - Inter-state flow analysis
4. **Resource Lab** - Capacity optimization
5. **System Health** - Anomaly detection

---

## 📈 Data Sources

| Dataset | Records | Description |
|---------|---------|-------------|
| Demographic | 2.07M | Age, population, pincode data |
| Biometric | 1.86M | Authentication records |
| Enrollment | 1.00M | New enrollments |
| **Total** | **4.93M** | Combined dataset |

---

## 🛠 Tech Stack

| Layer | Technologies |
|-------|--------------|
| **Frontend** | Tabler UI, Leaflet.js, Chart.js, ApexCharts |
| **Backend** | Flask, Python 3.x |
| **Data Processing** | Pandas, NumPy |
| **Maps** | OpenStreetMap + Leaflet.js |
| **AI/ML** | Custom forecasting algorithms |

---

## 📁 Project Structure

```
sankhya/
├── backend/
│   ├── app.py              # Flask server
│   ├── generate_data.py    # Data pre-processor
│   ├── ai_forecaster.py    # AI prediction model
│   ├── data_processor.py   # Analytics engine
│   └── requirements.txt    # Dependencies
├── data/
│   ├── sankhya_data.json   # Generated analytics
│   └── ai_forecast.json    # AI predictions
├── css/
│   └── custom.css          # Premium styling
├── images/
│   └── sankhya_logo.png    # Branding assets
├── index.html              # Main dashboard
├── login.html              # Authentication
└── [other pages].html      # Feature pages
```

---

## 🎨 Design Features

- 🇮🇳 Indian flag tricolor decorative strips
- Premium fonts (Poppins, Inter)
- Glassmorphism effects
- Dark/Light mode support
- Responsive layout

---

## 📐 DSI Formula

```
DSI = (V × Wa + S × Ws) / C + R

Where:
  V  = Transaction volume
  S  = Senior population ratio
  C  = Center capacity
  R  = Error rate
  Wa = Volume weight (0.4)
  Ws = Senior weight (0.3)
```

**Thresholds**:
- 🟢 Low: 0 - 3.3
- 🟡 Medium: 3.3 - 6.6
- 🔴 Critical: 6.6 - 10

---

## 👥 Team

Developed for **UIDAI Hackathon** - Predictive Governance Challenge

---

## 📄 License

MIT License

---

*Built with ❤️ for data-driven governance*
