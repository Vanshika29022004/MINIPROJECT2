# 🫀 Code Blue Co-Pilot

**Real-Time Cardiac Arrest Documentation & Clinical Guidance System**

A comprehensive AI-powered application designed to assist healthcare professionals during cardiac arrest emergencies by providing real-time clinical decision support, automated timing alerts, and complete documentation.

## ✨ Features

### 🔍 **Cardiac Arrest Detection**
- Machine learning model for real-time cardiac arrest prediction
- Analyzes vital signs (Heart Rate, SpO₂, Blood Pressure)
- Risk assessment with probability scoring

### 🎤 **Voice Input Processing**
- OpenAI Whisper AI integration for speech-to-text
- Real-time clinical event transcription
- Hands-free operation during emergencies

### ⚡ **ACLS Clinical Engine**
- Automated ACLS protocol guidance
- Real-time decision support for shockable vs non-shockable rhythms
- Evidence-based clinical recommendations

### 🚨 **Automatic Timer Alerts**
- CPR cycle monitoring (2-minute intervals)
- Epinephrine timing alerts (3-5 minute cycles)
- Multi-stage warnings (30s → 10s → critical)
- Visual and audio notifications

### 📊 **Real-Time Monitoring**
- Live event logging and timeline
- Session state management
- Automatic refresh during active code blue

### 📄 **Comprehensive Reporting**
- Text report generation
- PDF report export with FPDF2
- Complete clinical event documentation

## 🏗️ Architecture

```
code-blue-copilot/
├── app.py              # Main Streamlit application
├── detection.py        # ML cardiac arrest prediction
├── speech.py           # Voice transcription with Whisper
├── nlp_engine.py       # Clinical text processing
├── acls_engine.py      # ACLS protocol logic
├── timer.py            # Clinical timing with alerts
├── report.py           # Documentation generation
├── requirements.txt    # Python dependencies
├── models/             # ML model storage
└── venv/               # Virtual environment
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Git

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Vanshika29022004/MINIPROJECT2.git
cd MINIPROJECT2/code-blue-copilot
```

2. **Set up virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python -m streamlit run app.py
```

4. **Open in browser:**
```
http://localhost:8501
```

## 🔧 Technical Stack

- **Frontend:** Streamlit with custom CSS
- **AI/ML:** Scikit-learn, OpenAI Whisper
- **Data Processing:** NumPy, Pandas
- **Audio:** SoundDevice, SciPy
- **Reporting:** FPDF2
- **Environment:** Python virtual environment

## 📋 Usage Guide

### 1. Patient Assessment
- Enter vital signs (Heart Rate, SpO₂, BP)
- Click "Detect Cardiac Arrest"
- Review ML prediction and risk assessment

### 2. Code Blue Activation
- System automatically activates when cardiac arrest detected
- Clinical timer starts with automatic alerts
- Voice/text input for real-time event logging

### 3. Clinical Events
- Log interventions: "Epinephrine 1 mg given"
- Voice commands: Speak clinical actions
- System provides real-time ACLS guidance

### 4. Timer Alerts
- Automatic warnings for CPR cycles (2 min)
- Epinephrine timing alerts (3-5 min)
- Acknowledge alerts with ✅ button

### 5. Documentation
- Generate text reports
- Export PDF documentation
- Complete clinical timeline

## ⚠️ Medical Disclaimer

**This system is for decision support only, not a replacement for clinical judgment.**

- Always follow institutional ACLS protocols
- Consult qualified medical professionals
- Use as supplementary tool during emergencies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- **Vanshika Sharma** - *Initial work* - [GitHub](https://github.com/Vanshika29022004)

## 🙏 Acknowledgments

- OpenAI for Whisper AI technology
- Streamlit for the web framework
- Healthcare professionals for clinical guidance
- Medical research community for ACLS protocols

---

**🫀 Saving lives through technology - one heartbeat at a time**