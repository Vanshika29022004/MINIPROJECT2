// Socket IO integration
let socket = null;

function connectSocket() {
    socket = io(API_URL);

    socket.on('connect', () => {
        console.log('Socket connected securely.');
        const statusEl = document.getElementById('connection-status');
        statusEl.textContent = 'Connected';
        statusEl.className = 'status online';
    });

    socket.on('disconnect', () => {
        console.log('Socket disconnected.');
        const statusEl = document.getElementById('connection-status');
        statusEl.textContent = 'Disconnected';
        statusEl.className = 'status offline';
    });

    socket.on('directive_update', (data) => {
        const box = document.getElementById('active-directive');
        const text = document.querySelector('.directive-text');
        text.textContent = data.message;
        
        // Blink animation
        box.style.backgroundColor = 'rgba(239, 68, 68, 0.2)';
        box.style.borderColor = 'var(--accent-red)';
        setTimeout(() => {
            box.style.backgroundColor = 'rgba(59, 130, 246, 0.1)';
            box.style.borderColor = 'var(--accent-blue)';
        }, 1200);
    });

    socket.on('timer_tick', (data) => {
        const cprVal = document.querySelector('#timer-cpr .timer-value');
        const epiVal = document.querySelector('#timer-epi .timer-value');
        
        cprVal.textContent = data.cpr_time;
        epiVal.textContent = data.epi_time;
        
        if(data.cpr_alert) cprVal.style.color = 'var(--accent-red)';
        else cprVal.style.color = 'var(--text-primary)';
        
        if(data.epi_alert) epiVal.style.color = 'var(--accent-red)';
        else epiVal.style.color = 'var(--accent-yellow)';
    });
    
    socket.on('new_log_event', (data) => {
        if(window.addTimelineEvent) {
            // Helper defined in main.js
            let text = data.event_type;
            if(data.structured_data && Object.keys(data.structured_data).length > 0) {
               text += ` (${JSON.stringify(data.structured_data)})`; 
            }
            // Add native timestamp from backend
            const dateStr = new Date(data.timestamp).toLocaleTimeString();
            window.addTimelineEvent(text, dateStr);
        }
    });
}

window.socketManager = {
    connect: connectSocket
};
