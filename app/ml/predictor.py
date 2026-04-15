import os
import joblib
import pandas as pd

class MLPredictor:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MLPredictor, cls).__new__(cls)
            cls._instance._load_model()
        return cls._instance
        
    def _load_model(self):
        """Loads the serialized model on initialization."""
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'model.pkl')
        try:
            self.model = joblib.load(model_path)
        except Exception as e:
            print(f"Warning: Could not load model ({e}). Did you run train_model.py?")
            self.model = None

    def predict_risk(self, hr: float, spo2: float, sbp: float) -> dict:
        """
        Returns JSON-serializable dict of Risk Assessment.
        """
        if self.model is None:
            return {"risk_score": "--", "risk_level": "Unknown", "message": "Model not loaded"}
            
        # Create single row DataFrame
        X = pd.DataFrame([{
            'HR': float(hr),
            'SpO2': float(spo2),
            'SBP': float(sbp)
        }])
        
        # Predict Proba -> array of [prob_class_0, prob_class_1]
        probs = self.model.predict_proba(X)
        risk_pct = probs[0][1] * 100
        
        # Simple thresholding logic
        level = "Low"
        msg = "Patient is stable."
        if risk_pct > 75:
            level = "Severe"
            msg = "Imminent high risk. Prepare code blue cart."
        elif risk_pct > 30:
            level = "Elevated"
            msg = "Monitor patient closely."
            
        return {
            "risk_score": f"{risk_pct:.1f}%",
            "risk_level": level,
            "message": msg
        }
