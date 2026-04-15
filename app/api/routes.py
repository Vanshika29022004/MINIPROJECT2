from flask import Blueprint, request, jsonify
from app.ml.predictor import MLPredictor

bp = Blueprint('api', __name__, url_prefix='/api')

predictor = MLPredictor()

@bp.route('/predict', methods=['POST'])
def predict_risk():
    """Calculates code blue risk based on vital inputs."""
    data = request.json
    
    if not data:
        return jsonify({"error": "No input data provided"}), 400
        
    try:
        hr = data.get('hr', 0)
        spo2 = data.get('spo2', 100)
        sbp = data.get('sbp', 120)
        
        result = predictor.predict_risk(hr, spo2, sbp)
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@bp.route('/health', methods=['GET'])
def health_check():
    """Simple API health check."""
    return jsonify({"status": "Healthy", "version": "1.0.0"}), 200

@bp.route('/report', methods=['GET'])
def generate_report():
    """Generates the structured summary JSON of the code."""
    try:
        from app.core.reporter import reporter
        summary = reporter.generate_summary()
        return jsonify(summary), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from app.ml.nlp_pipeline import nlp
from app.core.acls_engine import acls
from app.core.reporter import reporter
from app.core.timer_system import timers
from flask import current_app

@bp.route('/event', methods=['POST'])
def ingest_event():
    """Ingests raw text, parses it, and forwards to ACLS engine & UI."""
    data = request.json
    
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
        
    try:
        raw_text = data['text']
        
        # 1. Start Code Logic Support
        if raw_text.lower() == "start code":
            timers.start_code()
            acls.reset()
            reporter.clear()
            return jsonify({"status": "Code Blue Started"}), 200
            
        if raw_text.lower() == "end code":
            timers.stop_code()
            return jsonify({"status": "Code Blue Ended"}), 200
            
        if raw_text.lower() == "reset code":
            timers.stop_code()
            acls.reset()
            reporter.clear()
            return jsonify({"status": "Code Blue Reset"}), 200
        
        # 2. NLP Processing
        structured_event = nlp.process_text(raw_text)
        
        # 3. Store in Report
        reporter.add_event(structured_event)
        
        # 4. Process state through ACLS Engine
        next_directive = acls.process_event(structured_event)
        
        # 5. Timer System Triggers
        e_type = structured_event.get("event_type")
        if e_type in ["Defibrillation", "CPR"]:
            timers.reset_cpr_timer()
        elif e_type == "Medication Administration" and structured_event.get("structured_data", {}).get("drug") == "Epinephrine":
            timers.reset_epi_timer()
        
        # 6. Emit via WebSockets immediately to UI
        from app import socketio # lazy import
        socketio.emit('new_log_event', structured_event)
        socketio.emit('directive_update', {'message': next_directive})
        
        return jsonify(structured_event), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
