# 📊 Thinklar CRM - Lead Capture System

A robust, enterprise-grade Lead Capture & Pipeline Management System (CRM Module) built to streamline sales workflows. This application automates lead capturing, filters data with partial matches, updates pipeline stages inline, and features a live business intelligence analytics dashboard.

---

## 📺 Project Demo Video
🔗 [Click Here to Watch the Live Application Demo Video](https://drive.google.com/file/d/1dh__onbS287eAMC41-aqmOLCWgPb-BfS/view?usp=sharing)

---

## ✨ Key Features Implemented

- **Power BI Style Analytics Dashboard:** Real-time summary cards mapping *Total, New, Contacted, Qualified, and Lost* counts instantly using fast optimized SQL queries.
- **Fail-Safe Input Validation:** Multi-layered security checks with custom HTML5 regex patterns for mobile structures, frontend type enforcements, and strict backend duplication blockguards.
- **Dynamic Search & Filtering:** Live querying mechanism enabling partial text tracking across Names, Company Profiles, and Mobile Numbers.
- **Inline Pipeline Transitioning:** High-speed status synchronization forms embedding dynamic state flags (`selected` preservation templates) directly into the UI.
- **Smooth Session Flash Feedback:** Real-time dismissible alert notices driven by integrated native JavaScript bindings.

---

## 🛠️ Tech Stack Utilized

- **Backend Architecture:** Python 3.x with Flask Framework
- **Database Engine:** MySQL Server (Relational Design)
- **Frontend Layer:** HTML5, Modern CSS3 Core, Bootstrap 5.3 Framework
- **Integration Layer:** Jinja2 Template Engine & MySQL Connector Python Drivers

---

## 📂 Project Directory Structure

```text
crm_project/
├── app.py                  # Main Flask application logic & routing engines
├── schema.sql              # Clean database relational setup script
├── templates/              # Jinja2 presentation layers
│   ├── index.html          # Core Analytics & Lead Grid Interface
│   └── add_lead.html       # Capture Validation Form Screen
├── README.md               # Professional Technical Documentation
└── .gitignore              # Production security exclusion file