import time
import eventlet
from flask_socketio import SocketIO

class TimerSystem:
    def __init__(self):
        self.code_active = False
        self.code_start_time = 0
        self.cycle_start_time = 0
        self.current_step = 0
        self.socketio = None
        self._timer_thread = None
        
        # Define the 2-minute cycle steps
        self.steps = [
            {"name": "CPR", "duration": 120, "directive": "Push hard and fast (100-120/min). Minimize interruptions."},
            {"name": "Rhythm Check", "duration": 10, "directive": "Check rhythm. If VF/pVT -> Shock. If Asystole/PEA -> Continue CPR."},
            {"name": "CPR", "duration": 120, "directive": "Resume CPR immediately for 2 minutes."},
            {"name": "Pulse Check", "duration": 10, "directive": "Check for return of spontaneous circulation (ROSC)."},
            {"name": "CPR", "duration": 120, "directive": "Continue CPR. Prepare for next cycle."},
            {"name": "Medication Window", "duration": 60, "directive": "Consider Epinephrine every 3-5 minutes if no ROSC."}
        ]
        
    def init_app(self, socketio: SocketIO):
        self.socketio = socketio
        
    def start_code(self):
        """Starts the global code timer and resets sub-timers."""
        self.code_active = True
        self.code_start_time = time.time()
        self.cycle_start_time = time.time()
        self.current_step = 0
        
        # Start background emit loop
        if self._timer_thread is None:
            self._timer_thread = self.socketio.start_background_task(self._timer_loop)
            
    def stop_code(self):
        """Halts all timers."""
        self.code_active = False
        self._timer_thread = None
        self.current_step = 0
        
    def reset_cpr_timer(self):
        """Reset CPR cycle to step 0."""
        self.cycle_start_time = time.time()
        self.current_step = 0
        
    def reset_epi_timer(self):
        """Epi timer - handled by step tracking."""
        pass
        
    def _format_time(self, seconds: int) -> str:
        m, s = divmod(seconds, 60)
        return f"{m:02d}:{s:02d}"
        
    def _timer_loop(self):
        """Background thread executing every second, emitting UI updates."""
        while self.code_active:
            now = time.time()
            cycle_elapsed = int(now - self.cycle_start_time)
            current_step_info = self.steps[self.current_step]
            step_duration = current_step_info["duration"]
            
            # Check if we need to advance to next step
            if cycle_elapsed >= step_duration:
                self.current_step = (self.current_step + 1) % len(self.steps)
                self.cycle_start_time = time.time()
                cycle_elapsed = 0
                
                # Emit step change notification
                new_step = self.steps[self.current_step]
                self.socketio.emit('step_change', {
                    'step_name': new_step["name"],
                    'step_index': self.current_step,
                    'directive': new_step["directive"],
                    'duration': new_step["duration"]
                })
            
            # Calculate time remaining in current step
            time_remaining = max(0, step_duration - cycle_elapsed)
            
            # Total code elapsed time
            total_elapsed = int(now - self.code_start_time)
            
            # Emit timer tick with step info
            self.socketio.emit('timer_tick', {
                'total_time': self._format_time(total_elapsed),
                'cycle_time': self._format_time(cycle_elapsed),
                'step_name': current_step_info["name"],
                'step_index': self.current_step,
                'time_remaining': self._format_time(time_remaining),
                'directive': current_step_info["directive"],
                'progress': int((cycle_elapsed / step_duration) * 100)
            })
            
            self.socketio.sleep(1)  # eventlet non-blocking sleep

# Global singleton
timers = TimerSystem()
