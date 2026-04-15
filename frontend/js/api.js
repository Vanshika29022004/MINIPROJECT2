// Dummy constants until we wire real APIs
const API_URL = 'http://localhost:5000';

async function fetchPrediction(data) {
    try {
        const response = await fetch(`${API_URL}/api/predict`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error('API request failed');
        return await response.json();
    } catch (error) {
        console.error("Error fetching prediction:", error);
        return { risk_score: "ERR", risk_level: "Error", message: "Failed to connect to API" };
    }
}

async function postEvent(text) {
    try {
        const response = await fetch(`${API_URL}/api/event`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        if (!response.ok) throw new Error('Failed to post event');
        return await response.json();
    } catch (error) {
        console.error("Error posting event:", error);
    }
}

async function getReport() {
    try {
        const response = await fetch(`${API_URL}/api/report`, { method: 'GET' });
        if(!response.ok) throw new Error("Failed to fetch report");
        return await response.json();
    } catch (error) {
        console.error("Error fetching report:", error);
    }
}

// Global expose
window.api = {
    fetchPrediction,
    postEvent,
    getReport
};
