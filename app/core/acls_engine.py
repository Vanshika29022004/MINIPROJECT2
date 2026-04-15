class ACLSEngine:
    def __init__(self):
        self.reset()
        
    def reset(self):
        """Resets engine for a new code blue."""
        self.shocks_delivered = 0
        self.epi_doses = 0
        self.amio_doses = 0
        self.current_directive = "Assess rhythm and pulse."
        self.rhythm_shockable = None

    def process_event(self, event: dict) -> str:
        """
        Receives structured event from NLP pipeline, updates state,
        and returns the next recommended directive.
        """
        e_type = event.get("event_type")
        data = event.get("structured_data", {})
        
        # 1. Defibrillation
        if e_type == "Defibrillation":
            self.shocks_delivered += 1
            self.current_directive = "Shock delivered. Resume CPR IMMEDIATELY (2 minutes)."
            
        # 2. Medication
        elif e_type == "Medication Administration":
            drug = data.get("drug")
            if drug == "Epinephrine":
                self.epi_doses += 1
                self.current_directive = f"Epinephrine given ({self.epi_doses}). Next dose in 3-5 mins. Continue CPR."
            elif drug == "Amiodarone":
                self.amio_doses += 1
                self.current_directive = "Amiodarone given. Consider reversible causes. Continue CPR."
                
        # 3. CPR Cycle / Pulse Check
        elif e_type == "Pulse Check" or e_type == "CPR":
            self.current_directive = "Assess Rhythm. If VF/pVT -> Shock. If Asystole/PEA -> Epi immediately."
            
        return self.current_directive

# Global singleton
acls = ACLSEngine()
