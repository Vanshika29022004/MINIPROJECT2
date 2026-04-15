import re
from datetime import datetime, timezone

class NLPPipeline:
    def __init__(self):
        # Dictionaries mapped to standard terminology
        self.medications = {
            r'\bepi(nephrine)?\b': 'Epinephrine',
            r'\bamio(darone)?\b': 'Amiodarone',
            r'\blido(caine)?\b': 'Lidocaine',
            r'\batropine\b': 'Atropine',
            r'\bmag(nesium)?\b': 'Magnesium'
        }
        
        self.actions = {
            r'\bshock\b|\bdefibrillate\b': 'Defibrillation',
            r'\bcpr\b|\bcompressions\b': 'CPR',
            r'\bintubat(?:e|ed|ion)\b': 'Intubation',
            r'\biv\b|\bio\b': 'Vascular Access',
            r'\bpulse check\b': 'Pulse Check'
        }
        
        # Regex to extract numeric values and units
        self.dosage_pattern = re.compile(r'(\d+(?:\.\d+)?)\s*(mg|mcg|J|joules|ml)')

    def process_text(self, text: str) -> dict:
        """
        Takes raw clinical text and extracts structured medical events.
        """
        text = text.lower()
        
        # Base event structure
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "raw_text": text,
            "event_type": "Log Note", # default
            "structured_data": {}
        }

        # 1. Check for specific actions
        for pattern, action_name in self.actions.items():
            if re.search(pattern, text):
                event["event_type"] = action_name
                break # Defaulting to first match for simplicity

        # 2. Check for medications
        for pattern, med_name in self.medications.items():
            if re.search(pattern, text):
                event["event_type"] = "Medication Administration"
                event["structured_data"]["drug"] = med_name
                break

        # 3. Extract dosages / Energy (Joules)
        dose_match = self.dosage_pattern.search(text)
        if dose_match:
            val, unit = dose_match.groups()
            event["structured_data"]["value"] = float(val)
            event["structured_data"]["unit"] = unit
            
        # Additional rule for shock energy specifically
        if event["event_type"] == "Defibrillation" and dose_match:
            event["structured_data"]["energy"] = event["structured_data"].pop("value")
            
        return event

# Singleton instance
nlp = NLPPipeline()
