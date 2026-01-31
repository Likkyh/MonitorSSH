# 🛡️ MonitorSSH - Log Analysis Dashboard

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**MonitorSSH** is an interactive security dashboard built with **Streamlit**. It allows administrators to visualize SSH connection events, identify aggressive IP addresses, and analyze security trends over time using parsed log data.

## ✨ Features

* **📊 Interactive Dashboard**: visualize security metrics with a clean, wide-layout interface.
* **🔍 Advanced Filtering**: Filter logs by **Date Range**, **Event ID**, or **Source IP**.
* **📈 Visual Analytics**:
    * **Aggressive IPs**: Bar charts identifying top potential attackers.
    * **Time Series**: Line charts showing attack frequency over time.
    * **Key Metrics**: Instant view of total events, unique IPs, and top targeted users.
* **📥 Data Export**: Download filtered datasets directly as CSV files.
* **⚡ Performance**: Uses caching to ensure fast load times for large datasets.

## 🛠️ Installation

### Prerequisites

* Python 3.8 or higher
* pip (Python Package Manager)

### Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/Likkyh/MonitorSSH.git](https://github.com/Likkyh/MonitorSSH.git)
    cd MonitorSSH
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
    *(If `requirements.txt` is missing, install manually: `pip install streamlit pandas`)*

3.  **Prepare your Data**
    Ensure your log file is placed at `src/datasetssh.csv`. The CSV must contain the following columns:
    * `Date et Heure` (Format: `dd/mm/yy - HH:MM:SS`)
    * `Identifiant Evenement`
    * `IP Source`
    * `Utilisateur Vise`

## 🚀 Usage

Run the dashboard using the Streamlit command line tools:

```bash
streamlit run app.py

The application will launch automatically in your default web browser (usually at http://localhost:8501).
📂 Project Structure
Plaintext

MonitorSSH/
├── src/
│   └── datasetssh.csv    # Input data file (Required)
├── app.py                # Main Dashboard logic
├── requirements.txt      # Python dependencies
└── README.md             # Documentation

📋 Data Format

The application expects a CSV file (src/datasetssh.csv) with specific column headers to function correctly. Ensure your CSV follows this structure:
Date et Heure	Identifiant Evenement	IP Source	Utilisateur Vise
10/12/25 - 06:55:46	Failed Password	192.168.1.50	root
10/12/25 - 06:56:00	Invalid User	10.0.0.5	admin
🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

    Fork the project

    Create your Feature Branch (git checkout -b feature/AmazingFeature)

    Commit your changes (git commit -m 'Add some AmazingFeature')

    Push to the Branch (git push origin feature/AmazingFeature)

    Open a Pull Request

📄 License

Distributed under the MIT License. See LICENSE for more information.
