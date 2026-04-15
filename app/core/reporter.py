import json

class ReportGenerator:
    def __init__(self):
        self.timeline = []
        
    def add_event(self, event: dict):
        self.timeline.append(event)
        
    def generate_summary(self) -> dict:
        """Parses the timeline into a structured post-code summary."""
        events = len(self.timeline)
        shocks = sum(1 for e in self.timeline if e.get('event_type') == 'Defibrillation')
        epi = sum(1 for e in self.timeline if e.get('event_type') == 'Medication Administration' and e.get('structured_data', {}).get('drug') == 'Epinephrine')
        
        return {
            "total_events_logged": events,
            "shocks_delivered": shocks,
            "epinephrine_doses": epi,
            "timeline": self.timeline
        }
        
    def clear(self):
        self.timeline = []

# Global Singleton
reporter = ReportGenerator()
