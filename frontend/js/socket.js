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

    // New step-based timer tick
    socket.on('timer_tick', (data) => {
        // Total code time
        const totalTimeEl = document.querySelector('#timer-total .timer-value');
        if (totalTimeEl) totalTimeEl.textContent = data.total_time;
        
        // Current cycle time
        const cycleTimeEl = document.querySelector('#timer-cycle .timer-value');
        if (cycleTimeEl) cycleTimeEl.textContent = data.cycle_time;
        
        // Time remaining in current step
        const remainingEl = document.querySelector('.time-remaining');
        if (remainingEl) remainingEl.textContent = data.time_remaining;
        
        // Current step name
        const stepNameEl = document.querySelector('.current-step-name');
        if (stepNameEl) stepNameEl.textContent = data.step_name;
        
        // Directive
        const directiveEl = document.querySelector('.directive-text');
        if (directiveEl) directiveEl.textContent = data.directive;
        
        // Progress bar
        const progressBar = document.querySelector('.step-progress-fill');
        if (progressBar) progressBar.style.width = data.progress + '%';
        
        // Step indicator styling
        const stepContainer = document.querySelector('.step-indicator');
        if (stepContainer) {
            const steps = stepContainer.querySelectorAll('.step-item');
            steps.forEach((step, index) => {
                if (index === data.step_index) {
                    step.classList.add('active');
                } else {
                    step.classList.remove('active');
                }
            });
        }
        
        // Alert for step change
        if (data.step_index === 0 || data.step_index === 2 || data.step_index === 4) {
            // CPR steps - red highlight
            const timerBox = document.querySelector('.timer-display');
            if (timerBox) timerBox.style.borderColor = 'var(--accent-red)';
        } else {
            const timerBox = document.querySelector('.timer-display');
            if (timerBox) timerBox.style.borderColor = 'var(--accent-blue)';
        }
    });
    
    // Step change notification
    socket.on('step_change', (data) => {
        const box = document.getElementById('active-directive');
        const text = document.querySelector('.directive-text');
        text.textContent = data.directive;
        
        // Flash animation for step change
        box.style.backgroundColor = 'rgba(239, 68, 68, 0.3)';
        box.style.borderColor = 'var(--accent-red)';
        setTimeout(() => {
            box.style.backgroundColor = 'rgba(59, 130, 246, 0.1)';
            box.style.borderColor = 'var(--accent-blue)';
        }, 1500);
        
        // Add timeline event for step change
        if (window.addTimelineEvent) {
            window.addTimelineEvent(`Step: ${data.step_name}`, new Date().toLocaleTimeString());
        }
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
