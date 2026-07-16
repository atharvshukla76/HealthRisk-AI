document.getElementById('clinical-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const btn = document.getElementById('analyze-btn');
    const idleState = document.getElementById('idle-state');
    const loadState = document.getElementById('loading-state');
    const resultState = document.getElementById('results-state');
    
    const riskPercentage = document.getElementById('risk-percentage');
    const riskTier = document.getElementById('risk-tier');
    const riskRecommendation = document.getElementById('clinical-recommendation');
    const riskCircle = document.getElementById('risk-circle');

    // Get ALL inputs for the new, smarter AI model
    const age = parseFloat(document.getElementById('age').value);
    const gender = document.getElementById('gender').value;
    const weight = parseFloat(document.getElementById('weight').value);
    const bp = document.getElementById('bp').value || "120/80";
    const hr = parseFloat(document.getElementById('hr').value) || 72;
    const smoker = document.getElementById('smoker').value;

    btn.innerText = "Analyzing Vitals...";
    btn.disabled = true;
    idleState.classList.add('hidden');
    resultState.classList.add('hidden');
    loadState.classList.remove('hidden');

    try {
        const response = await fetch('http://127.0.0.1:8000/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ age, gender, weight, bp, hr, smoker })
        });

        const data = await response.json();
        const percentage = Math.round(data.risk_probability * 100);

        setTimeout(() => {
            loadState.classList.add('hidden');
            resultState.classList.remove('hidden');
            
            riskPercentage.innerText = `${percentage}%`;
            
            riskCircle.classList.remove('status-critical', 'status-critical-bg');
            riskPercentage.classList.remove('status-critical');
            riskTier.classList.remove('status-critical');

            if (data.high_risk || percentage > 70) {
                riskCircle.classList.add('status-critical', 'status-critical-bg');
                riskPercentage.classList.add('status-critical');
                riskTier.classList.add('status-critical');
                riskTier.innerText = "CRITICAL RISK";
                riskRecommendation.innerText = `Warning: Model detects high correlation with adverse events based on ${bp} blood pressure and patient vitals. Immediate secondary screening is recommended.`;
            } else {
                riskTier.innerText = "NORMAL PROFILE";
                riskRecommendation.innerText = `Patient profile does not currently indicate a high risk of adverse clinical outcomes. Routine monitoring is sufficient at this time.`;
                riskTier.style.color = "#10b981";
            }

            btn.innerText = "Run AI Risk Analysis";
            btn.disabled = false;
        }, 1500);

    } catch (error) {
        console.error("API Error:", error);
        loadState.classList.add('hidden');
        idleState.classList.remove('hidden');
        idleState.innerHTML = "<p style='color: #ef4444;'>Connection Error. Ensure FastAPI is running on port 8000.</p>";
        btn.innerText = "Run AI Risk Analysis";
        btn.disabled = false;
    }
});