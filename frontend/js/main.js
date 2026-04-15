document.addEventListener('DOMContentLoaded', () => {
    // 1. Establish Socket Connection
    // setTimeout to ensure CDNs and scripts loaded (naive fallback)
    if(window.socketManager) {
        window.socketManager.connect();
    }

    // 2. Bind DOM Elements
    const vitalsForm = document.getElementById('vitals-form');
    const riskDisplay = document.getElementById('risk-display');
    const riskValue = document.getElementById('risk-score-value');
    
    const eventBtn = document.getElementById('btn-submit-event');
    const clinicalInput = document.getElementById('clinical-input');
    const timelineList = document.getElementById('event-timeline');

    // 3. Vitals Form Submit Handler
    vitalsForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const hr = document.getElementById('input-hr').value;
        const spo2 = document.getElementById('input-spo2').value;
        const sbp = document.getElementById('input-sbp').value;

        // Mock fetch from API
        if (window.api) {
            const res = await window.api.fetchPrediction({hr, spo2, sbp});
            riskValue.textContent = res.risk_score;
            riskDisplay.classList.remove('hidden');
        }
    });

    // 4. Clinical Event Submit Handler
    eventBtn.addEventListener('click', async () => {
        const text = clinicalInput.value.trim();
        if (!text) return;

        if(window.api) {
            await window.api.postEvent(text);
            clinicalInput.value = '';
        }
    });
    
    // Support enter key
    clinicalInput.addEventListener('keypress', (e) => {
        if(e.key === 'Enter') eventBtn.click();
    });

    // 5. Code Blue State Helpers
    document.getElementById('btn-start-code').addEventListener('click', async (e) => {
        const btn = e.target;
        if(btn.textContent === 'START CODE BLUE') {
            btn.textContent = 'END CODE BLUE';
            btn.classList.replace('critical', 'action');
            if(window.api) await window.api.postEvent("start code");
            addTimelineEvent("Code Blue Initiated", new Date().toLocaleTimeString());
            document.getElementById('btn-generate-report').classList.add('hidden');
            document.getElementById('btn-reset-session').classList.add('hidden');
        } else {
            btn.textContent = 'START CODE BLUE';
            btn.classList.replace('action', 'critical');
            if(window.api) await window.api.postEvent("end code");
            document.querySelector('.directive-text').textContent = "Code Concluded. Post-resuscitation care.";
            addTimelineEvent("Code Blue Concluded", new Date().toLocaleTimeString());
            document.getElementById('btn-generate-report').classList.remove('hidden');
            document.getElementById('btn-reset-session').classList.remove('hidden');
        }
    });
    
    // 6. Generate Report
    document.getElementById('btn-generate-report').addEventListener('click', async () => {
        if(window.api) {
            const report = await window.api.getReport();
            
            // Format the report into a nice text document
            let docStr = "=== CODE BLUE POST-EVENT REPORT ===\n\n";
            docStr += "SUMMARY STATISTICS:\n";
            docStr += `Total Events Logged: ${report.total_events_logged}\n`;
            docStr += `Shocks Delivered: ${report.shocks_delivered}\n`;
            docStr += `Epinephrine Doses: ${report.epinephrine_doses}\n\n`;
            
            docStr += "--- CHRONOLOGICAL TIMELINE ---\n";
            report.timeline.forEach(event => {
                const time = new Date(event.timestamp).toLocaleTimeString();
                let eventData = event.event_type;
                if (event.structured_data && Object.keys(event.structured_data).length > 0) {
                    eventData += ` (${JSON.stringify(event.structured_data)})`;
                }
                docStr += `[${time}] ${eventData}\n`;
            });
            
            docStr += "\n=== END OF REPORT ===";
            
            // Create a downloadable Blob
            const blob = new Blob([docStr], { type: 'text/plain' });
            const url = window.URL.createObjectURL(blob);
            
            // Trigger hidden download link
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            // Name file with current timestamp
            const dateStr = new Date().toISOString().replace(/[:.]/g, '-').split('T');
            a.download = `CodeBlue_Report_${dateStr[0]}_${dateStr[1]}.txt`;
            
            document.body.appendChild(a);
            a.click();
            
            // Cleanup
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        }
    });

    // 7. Reset Session
    document.getElementById('btn-reset-session').addEventListener('click', async () => {
        if(confirm("Are you sure you want to reset the session? All current data will be cleared.")) {
            if(window.api) await window.api.postEvent("reset code");
            
            // Clear Vitals
            document.getElementById('vitals-form').reset();
            document.getElementById('risk-display').classList.add('hidden');
            
            // Clear Timeline
            timelineList.innerHTML = '';
            
            // Clear Timers and Directives
            document.querySelector('.directive-text').textContent = "Awaiting initiating event...";
            document.querySelector('#timer-cpr .timer-value').textContent = "00:00";
            document.querySelector('#timer-epi .timer-value').textContent = "00:00";
            document.querySelector('#timer-cpr .timer-value').style.color = "var(--text-primary)";
            document.querySelector('#timer-epi .timer-value').style.color = "var(--accent-yellow)";
            
            // Re-hide action buttons
            document.getElementById('btn-generate-report').classList.add('hidden');
            document.getElementById('btn-reset-session').classList.add('hidden');
        }
    });

    // Helper Function (assigned to window for socket.js access)
    window.addTimelineEvent = function(text, time) {
        const li = document.createElement('li');
        li.className = 'timeline-item';
        li.innerHTML = `
            <span class="time-stamp">${time}</span>
            <div class="event-details">${text}</div>
        `;
        // Insert at top
        timelineList.insertBefore(li, timelineList.firstChild);
    }
});
