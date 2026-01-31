# 🛡️ MonitorSSH - SSH Log Analysis Dashboard

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

**MonitorSSH** is an interactive security dashboard built with **Streamlit** that enables system administrators to visualize, analyze, and monitor SSH connection events from parsed log files. It helps identify suspicious activity, aggressive IP addresses, and security trends over time.
The sole purpose of this repo is to archive the exercise.
---

## 📑 Table of Contents

- [Features](#-features)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Installation](#️-installation)
- [Data Format](#-data-format)
- [Usage](#-usage)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 📊 **Interactive Dashboard** | Wide-layout interface with tabs for visual analytics and raw data |
| 🔍 **Advanced Filtering** | Filter logs by date range, event type, or source IP addresses |
| 📈 **Visual Analytics** | Bar charts for top aggressive IPs, line charts for attack frequency over time |
| 📋 **Key Metrics** | Instant view of total events, unique IPs, and most targeted users |
| 📥 **CSV Export** | Download filtered datasets for offline analysis |
| ⚡ **Cached Performance** | Uses `@st.cache_data` for fast load times with large datasets |

---

## 🔧 How It Works

The application follows a simple data flow:

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────────┐
│  CSV Log File   │────▶│  Data Loading   │────▶│  Filtering Engine  │
│ (datasetssh.csv)│     │  (Cached/Parsed) │     │  (Date/Event/IP)    │
└─────────────────┘     └──────────────────┘     └──────────┬──────────┘
                                                            │
                        ┌───────────────────────────────────┘
                        ▼
    ┌────────────────────────────────────────────────────────────┐
    │                     STREAMLIT DASHBOARD                    │
    │  ┌──────────────────────┐  ┌─────────────────────────────┐ │
    │  │   📈 Dashboard Tab   │  │     📋 Raw Data Tab        │ │
    │  │  • Key Metrics       │  │  • Filtered DataTable       │ │
    │  │  • Top 5 Aggressive  │  │  • CSV Export Button        │ │
    │  │    IPs (Bar Chart)   │  │                             │ │
    │  │  • Attack Frequency  │  │                             │ │
    │  │    (Line Chart)      │  │                             │ │
    │  └──────────────────────┘  └─────────────────────────────┘ │
    └────────────────────────────────────────────────────────────┘
```

### Core Components

1. **`load_data()`** - Cached function that:
   - Reads the CSV file from `src/datasetssh.csv`
   - Parses the `Date et Heure` column to datetime format (`dd/mm/yy - HH:MM:SS`)
   - Handles file errors gracefully with user-friendly messages

2. **Sidebar Filters** - Three filtering mechanisms:
   - **Date Range**: Select start and end dates from the dataset
   - **Event ID**: Dropdown to filter by event type (e.g., "Failed Password", "Invalid User")
   - **Source IP**: Multi-select for specific IP addresses

3. **Dashboard Tab** - Displays:
   - **Key Metrics**: Total events, unique IPs, most targeted user
   - **Top 5 Aggressive IPs**: Bar chart visualization
   - **Attack Frequency Over Time**: Daily resampled line chart

4. **Raw Data Tab** - Provides:
   - Interactive filtered data table
   - CSV download button for exporting filtered results

---

## 📂 Project Structure

```plaintext
MonitorSSH/
│
├── src/
│   └── datasetssh.csv      # 📄 Input CSV log file (Required)
│
├── app.py                  # 🚀 Main Streamlit application
│                           #    - Page configuration
│                           #    - Data loading (cached)
│                           #    - Filtering logic
│                           #    - Dashboard rendering
│
├── requirements.txt        # 📦 Python dependencies
│                           #    (streamlit, pandas)
│
└── README.md               # 📖 Project documentation
```

### File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | The main application entry point. Contains all dashboard logic including data loading, filtering, visualization, and UI components (~130 lines) |
| `src/datasetssh.csv` | The input dataset containing parsed SSH log entries. Must follow the required column format (see [Data Format](#-data-format)) |
| `requirements.txt` | Lists Python package dependencies (`streamlit`, `pandas`) |

---

## 🛠️ Installation

### Prerequisites

- **Python 3.8** or higher
- **pip** (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Likkyh/MonitorSSH.git
   cd MonitorSSH
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install manually:
   ```bash
   pip install streamlit pandas
   ```

4. **Add your log data**  
   Place your parsed SSH log file at `src/datasetssh.csv` (see format below)

---

## 📋 Data Format

The application expects a CSV file at `src/datasetssh.csv` with the following **required columns**:

| Column Name | Description | Example |
|-------------|-------------|---------|
| `Date et Heure` | Timestamp of the event | `10/12/25 - 06:55:46` |
| `Identifiant Evenement` | Type of SSH event | `Failed Password`, `Invalid User` |
| `IP Source` | Origin IP address | `192.168.1.50` |
| `Utilisateur Vise` | Targeted username | `root`, `admin` |

### Example CSV Content

```csv
Date et Heure,Identifiant Evenement,IP Source,Utilisateur Vise
10/12/25 - 06:55:46,Failed Password,192.168.1.50,root
10/12/25 - 06:56:00,Invalid User,10.0.0.5,admin
10/12/25 - 07:12:33,Failed Password,203.0.113.42,root
10/12/25 - 07:15:20,Invalid User,198.51.100.23,guest
```

> ⚠️ **Important**: The date format must be exactly `dd/mm/yy - HH:MM:SS` for proper parsing.

---

## 🚀 Usage

1. **Launch the dashboard**
   ```bash
   streamlit run app.py
   ```

2. **Access the application**  
   The dashboard opens automatically in your browser at `http://localhost:8501`

3. **Explore the data**
   - Use the **sidebar filters** to narrow down events
   - Switch between **Dashboard** and **Raw Data** tabs
   - **Download** filtered results using the export button

---

## 📸 Screenshots

*Dashboard overview with key metrics and visualizations*

| Dashboard Tab | Raw Data Tab |
|---------------|--------------|
| Key metrics, aggressive IPs chart, time series | Interactive data table with export |

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.
