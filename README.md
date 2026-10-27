# Electric Vehicle Market Performance & Insights ⚡

A complete, production-ready full-stack web application designed for executive market intelligence, strategic battery technology benchmarking, and consumer mobility research across the global electric vehicle industry.

---

## 🌟 Executive Summary & Problem Scenarios

The EV transition is reshaping global manufacturing, battery supply chains, and consumer adoption patterns. This platform is engineered to directly solve the operational workflows and decision-making imperatives of three core executive personas:

| Stakeholder Persona | Organizational Role | Core Strategic Mandate | Analytical Focus & Dashboard Deliverables |
| :--- | :--- | :--- | :--- |
| **Emily Johnson** | **EV Market Strategy Director** | Formulate 3-5 year technology roadmaps, cell chemistry sourcing, and pack cost optimization ($/kWh). | • Battery chemistry market share (LFP vs NMC vs NCA vs Solid-State)<br>• Pack cost-per-kWh benchmark and driving range correlation<br>• Adoption matrix across vehicle categories |
| **David Chen** | **Business Intelligence Manager** | Map global industrial manufacturing footprint, evaluate cross-border production, and track OEM delivery share. | • Country-wise EV sales volume and assembly capacity<br>• Top 10 global manufacturers by market delivery share<br>• Origin country vs vehicle category production breakdown |
| **Dr. Sarah Williams** | **Sustainable Mobility Research Analyst** | Assess consumer satisfaction drivers, charging convenience vs range anxiety, and lifecycle efficiency. | • Driving range span and benchmarks by vehicle category<br>• Charging speed tiers (<50 kW, 50-149 kW, 150-249 kW, 250+ kW) vs owner satisfaction<br>• Sustainable mobility leaders matrix (Rating ≥ 4.6 & Range ≥ 450 km) |

---

## 🏗️ System Architecture

```
                       ┌──────────────────────────────────────────────┐
                       │           Web Browser (Client)               │
                       │  Bootstrap 5 • Chart.js 4 • Dynamic Filters  │
                       └──────────────────────┬───────────────────────┘
                                              │ HTTP / JSON API
                                              ▼
                       ┌──────────────────────────────────────────────┐
                       │          Flask Application (app.py)          │
                       │  Routes • Parameter Parsing • JSON Endpoints │
                       └──────────────────────┬───────────────────────┘
                                              │ Python Calls
                                              ▼
                       ┌──────────────────────────────────────────────┐
                       │      SQL Operations (sql_operations.py)      │
                       │ Aggregations • Grouping • Parameterized SQL  │
                       └──────────────────────┬───────────────────────┘
                                              │ Fast Local Queries
                                              ▼
                       ┌──────────────────────────────────────────────┐
                       │           SQLite Database (database.db)       │
                       │  Indexed ev_market Table • 100+ Models       │
                       └──────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```text
EV-MARKET-INSIGHTS/
│
├── app.py                  # Flask backend web application & REST API routes
├── generate_data.py        # Realistic EV market data generator & database seeder
├── sql_operations.py       # Reusable SQL analytics engine & CLI reporting tool
├── database.db             # Local SQLite database containing simulated global EV records
├── requirements.txt        # Python package dependencies (Flask, Werkzeug)
├── README.md               # Comprehensive documentation and operational guide
│
├── templates/              # Jinja2 HTML5 Templates (Bootstrap 5)
│   ├── base.html           # Unified master layout, navigation, modal & theme switcher
│   ├── index.html          # Unified executive dashboard with all 6 charts & data table
│   ├── emily.html          # Dedicated strategic briefing view for Emily Johnson
│   ├── david.html          # Dedicated manufacturing BI view for David Chen
│   └── sarah.html          # Dedicated mobility research lab for Dr. Sarah Williams
│
└── static/                 # Static Assets
    ├── css/
    │   └── style.css       # Clean-tech CSS with dark/light mode and glassmorphism styling
    └── js/
        └── dashboard.js    # Chart.js engine, live AJAX filtering, sorting & modal handler
```

---

## 🗄️ Database Schema & Data Modeling

The application leverages a high-performance, normalized SQLite database table named `ev_market` with strategic B-tree indices on key query filters:

```sql
CREATE TABLE ev_market (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    manufacturer TEXT NOT NULL,              -- e.g. Tesla, BYD, Volkswagen, BMW, Rivian, Hyundai
    model TEXT NOT NULL,                     -- e.g. Model Y, Seal, ID.4 Pro, Ioniq 5 AWD
    vehicle_category TEXT NOT NULL,          -- Hatchback, Sedan, SUV, Two-Wheeler
    battery_tech TEXT NOT NULL,              -- LFP, NMC, NCA, Solid-State
    battery_capacity REAL NOT NULL,          -- Gross battery pack capacity in kWh
    driving_range INTEGER NOT NULL,          -- Certified real-world driving range in km
    price INTEGER NOT NULL,                  -- MSRP base retail price in USD
    charging_speed REAL NOT NULL,            -- Peak DC fast-charging rate in kW
    manufacturing_country TEXT NOT NULL,     -- Origin country (China, USA, Germany, etc.)
    customer_rating REAL NOT NULL,           -- Owner satisfaction score (1.0 to 5.0)
    annual_sales INTEGER NOT NULL,           -- Annual global unit delivery volume
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Performance Indices
CREATE INDEX idx_mfr ON ev_market(manufacturer);
CREATE INDEX idx_category ON ev_market(vehicle_category);
CREATE INDEX idx_battery ON ev_market(battery_tech);
CREATE INDEX idx_country ON ev_market(manufacturing_country);
CREATE INDEX idx_price ON ev_market(price);
```

---

## 🚀 Setup & Installation Instructions

### Prerequisites
- Python 3.9+ (Python 3.11 or 3.12 recommended)
- `pip` package manager

### 1. Clone or Navigate to the Project Directory
```powershell
cd c:\Users\goura\OneDrive\Desktop\EV-MARKET-INSIGHTS
```

### 2. (Optional) Create and Activate a Virtual Environment
```powershell
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Initialize Database & Populate Seed Data
```powershell
python generate_data.py
```
*Output: Generates over 100+ realistic EV models across diverse categories with accurate battery capacity, range, and sales distribution.*

### 5. (Optional) Run SQL Analytics CLI Verification
```powershell
python sql_operations.py
```
*Executes and prints the essential SQL queries directly to the console.*

### 6. Launch the Web Application
```powershell
python app.py
```
Open your browser and navigate to:
```
http://127.0.0.1:5000/
```

---

## 📊 Analytical Views & Core Capabilities

### 1. Unified Executive Dashboard (`/`)
- **Global KPI Counters**: Total Deliveries, Model Count, Average Driving Range (km), Average Pack Size (kWh), Market Leader OEM, Average Owner Rating.
- **Dynamic Multi-Criteria Filters**:
  - Search by Brand / Model Name (real-time 300ms debounce)
  - Vehicle Category (Hatchback, Sedan, SUV, Two-Wheeler)
  - Battery Technology (LFP, NMC, NCA, Solid-State)
  - Manufacturing Country (China, USA, Germany, South Korea, Japan, India, etc.)
  - Price Range Slider ($1,200 – $118,000+)
- **Interactive Visualizations (Chart.js)**:
  1. *Battery Chemistry Market Share* (Doughnut)
  2. *Cost Efficiency ($/kWh) vs Range (km)* (Multi-axis Bar)
  3. *Manufacturing Output by Country* (Horizontal Bar)
  4. *Top Global Manufacturers by Deliveries* (Bar)
  5. *Range Envelope by Category (Min/Avg/Max)* (Grouped Bar)
  6. *Charging Speed Tiers vs Owner Satisfaction* (Area/Line)
- **Live Data Explorer**:
  - Client & server-side sorting on all 11 columns
  - Pagination controls (10, 20, 50 rows per page)
  - Vehicle Specs Modal (one-click detailed drill-down)
  - CSV Export inheriting active filter parameters

### 2. Stakeholder Dedicated Workspaces
- **Emily Johnson Workspace (`/persona/emily`)**: Strategic battery chemistry roadmap, $/kWh and km/kWh calculations, and next-generation Solid-State adoption curves.
- **David Chen Workspace (`/persona/david`)**: Manufacturing hubs, cross-border supply chains, ASP differentials, and OEM volume dominance.
- **Dr. Sarah Williams Lab (`/persona/sarah`)**: The 150 kW fast-charging satisfaction inflection point, range utility diminishing returns, and two-wheeler urban efficiency metrics.

---

## 🔌 REST API Endpoints

| Endpoint | Method | Query Parameters | Description |
| :--- | :--- | :--- | :--- |
| `/api/kpis` | `GET` | `battery_tech`, `vehicle_category`, `country`, `max_price`, `search` | Returns calculated market KPIs matching filters. |
| `/api/emily` | `GET` | Same as above | Returns battery chemistry breakdown, cost metrics, and adoption matrix. |
| `/api/david` | `GET` | Same as above | Returns country assembly metrics, top OEM rankings, and category distributions. |
| `/api/sarah` | `GET` | Same as above | Returns category range spans, charging speed tiers, and high-satisfaction models. |
| `/api/models` | `GET` | `page`, `page_size`, `sort_by`, `sort_order`, + filter params | Returns paginated, sorted vehicle models for the interactive data table. |
| `/api/model/<id>` | `GET` | None | Returns single model technical specs for modal preview. |
| `/api/export` | `GET` | Same as filter params | Generates and downloads a CSV export of the filtered EV dataset. |

---

## 🎨 Design & Accessibility
- **Dual Theme Support**: Integrated dark/light mode toggle with persistence in `localStorage`.
- **Responsive Layout**: Designed mobile-first using Bootstrap 5 fluid grid system.
- **Accessibility & UX**: Semantic HTML5 tags, color-coded chemistry and category badges, and high-contrast typography.
