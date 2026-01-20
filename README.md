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
SCREENSHOTS FOR THE WEBSITE <img width="1366" height="609" alt="setting" src="https://github.com/user-attachments/assets/7c7d8abb-4ab0-46eb-81cd-1fb88b2784fe" />
<img width="1366" height="613" alt="resource lab" src="https://github.com/user-attachments/assets/520ab1b4-2b11-48b7-a29b-48b5879da708" />
<img width="1366" height="609" alt="reports" src="https://github.com/user-attachments/assets/a6b4f36d-8c7c-4a1d-957c-d516c141f343" />
<img width="1366" height="610" alt="migration" src="https://github.com/user-attachments/assets/18d50dfb-ca2f-499c-bf34-dbab26d68a97" />

<img width="1366" height="609" alt="login" src="https://github.com/user-attachments/assets/9b8478c8-6346-4cdd-93ad-5e50cabe7c5e" />
<img width="1366" height="611" alt="demographic" src="https://github.com/user-attachments/assets/f1be0306-dd53-4dc5-a50d-086afb75359b" />
<img width="1366" height="609" alt="dashboard3" src="https://github.com/user-attachments/assets/6064fe85-10d1-4f84-81d8-96e03c69f8b1" />
<img width="1366" height="611" alt="dashboard2" src="https://github.com/user-attachments/assets/4aefd22e-66ea-4b8d-9e8a-4d10590213cc" />

<img width="1366" height="610" alt="dashboard" src="https://github.com/user-attachments/assets/0c9b5299-6609-4c0b-b217-7d9889ac07eb" />
<img width="1366" height="612" alt="system health" src="https://github.com/user-attachments/assets/2747103d-5ffc-44af-96dc-1f6442bdad54" />

Developed for **UIDAI Hackathon** - Predictive Governance Challenge

---


## 📄 License

MIT License

---

*Built with ❤️ for data-driven governance*

