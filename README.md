# ENKO Road Map 2026 — Operational Dashboard (V1.1)

This repository contains **Version 1.1** of the **ENKO Operational Road Map 2026 Dashboard**, developed using **Streamlit** and **Altair**.

The dashboard transforms an operational planning Google Sheet into a **high-fidelity, executive-level Gantt-style visualization**, accessible through a web interface and updated in real time.

---

## 🎯 Purpose

The main objective of this dashboard is to:

- Provide a **clear, visual overview** of ENKO’s operational initiatives throughout 2026.
- Group initiatives by **strategic component** using swimlanes.
- Serve as a **decision-support tool** for planning, monitoring, and alignment.

---

## 🚀 Key Features

- Annual **Gantt-style roadmap (2026)**.
- Swimlanes grouped by strategic component:
  - Alianzas
  - Comunidad
  - Redes Sociales
  - Tecnología
  - Procesos
- Fixed, corporate color palette per component.
- Clean, light, **SaaS-style UI** suitable for executive audiences.
- Tooltips with initiative details.
- **Live data connection** to Google Sheets (public CSV export).

---

## 🧩 Technical Stack

- **Language:** Python 3
- **Framework:** Streamlit
- **Visualization:** Altair (Vega-Lite)
- **Data Source:** Google Sheets (CSV export)
- **Deployment:** Streamlit Cloud

---

## 📁 Repository Structure

```text
enko_roadmap/
├── app.py              # Main Streamlit application (V1.1)
├── requirements.txt    # Python dependencies
├── .gitignore          # Ignored local/system files
└── README.md           # Project documentation
🔄 Data Updates & Refresh Behavior
This version does not use caching (st.cache_data was intentionally removed).

```
As a result:

Every page refresh:

Re-reads the Google Sheets source.

Reflects the most recent roadmap updates automatically.

No server restart or manual cache clearing is required.

This behavior is intentional to support an evolving operational roadmap.

## 🛠️ Local Execution (Optional)
To run the dashboard locally:

bash
Copiar código
pip install -r requirements.txt
streamlit run app.py

## 🧭 Project Status
Current version: V1.1 (stable baseline)
- Scope: Annual operational roadmap visualization
- Executive summary view

## 📌 Notes
*This dashboard is designed as a planning and alignment tool, not as a real-time KPI or performance tracking system.*

