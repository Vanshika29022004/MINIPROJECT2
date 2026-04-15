import time
import eventlet
from flask_socketio import SocketIO

class TimerSystem:
    def __init__(self):
        self.code_active = False
        self.cpr_start_time = 0
        self.epi_start_time = 0
        self.socketio = None
        self._cpr_thread = None
        
    def init_app(self, socketio: SocketIO):
        self.socketio = socketio
        
    def start_code(self):
        """Starts the global code timer and resets sub-timers."""
        self.code_active = True
        self.cpr_start_time = time.time()
        self.epi_start_time = 0 # Epi timer starts on first dose
        
        # Start background emit loop
        if self._cpr_thread is None:
            self._cpr_thread = self.socketio.start_background_task(self._timer_loop)
            
    def stop_code(self):
        """Halts all timers."""
        self.code_active = False
        self._cpr_thread = None
        
    def reset_cpr_timer(self):
        self.cpr_start_time = time.time()
        
    def reset_epi_timer(self):
        self.epi_start_time = time.time()
        
    def _format_time(self, seconds: int) -> str:
        m, s = divmod(seconds, 60)
        return f"{m:02d}:{s:02d}"
        
    def _timer_loop(self):
        """Background thread executing every second, emitting UI updates."""
        while self.code_active:
            now = time.time()
            
            # 1. CPR Timer (Alert at 120 seconds)
            cpr_elapsed = int(now - self.cpr_start_time)
            cpr_format = self._format_time(cpr_elapsed)
            
            if cpr_elapsed >= 120 and cpr_elapsed % 5 == 0:
                # Every 5 seconds after 2 mins, pulse an alert directive
                self.socketio.emit('directive_update', {'message': 'PULSE CHECK: 2 minutes of CPR completed.'})
                
            # 2. Epi Timer (Alert after 3 mins / 180 seconds)
            epi_format = "00:00"
            if self.epi_start_time > 0:
                epi_elapsed = int(now - self.epi_start_time)
                epi_format = self._format_time(epi_elapsed)
                if epi_elapsed >= 180 and epi_elapsed % 15 == 0:
                    self.socketio.emit('directive_update', {'message': 'MED REMINDER: Consider Epinephrine (3 mins elapsed).'})

            # Emit ticker
            self.socketio.emit('timer_tick', {
                'cpr_time': cpr_format,
                'epi_time': epi_format,
                'cpr_alert': cpr_elapsed >= 120,
                'epi_alert': self.epi_start_time > 0 and (now - self.epi_start_time) >= 180
            })
            
            self.socketio.sleep(1) # eventlet non-blocking sleep

# Global singleton
timers = TimerSystem()
