from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    job_text = data.get('text', '').lower()
    
    # --- SCANNING LOGIC ---
    score = 0
    breakdown = []
    verify_flags = []
    
    # 1. Verify Company Logic
    if "@gmail.com" in job_text or "@yahoo.com" in job_text:
        score += 25
        verify_flags.append("Generic Email")
        breakdown.append({"label": "Used Gmail/Yahoo (Non-corporate)", "pts": -25})
        
    if "telegram" in job_text or "whatsapp" in job_text:
        score += 30
        verify_flags.append("Anonymous Chat")
        breakdown.append({"label": "Telegram/WhatsApp only contact", "pts": -30})

    # 2. Pattern Detection
    scam_keywords = [
        ("fee", 40, "Financial Request"),
        ("check", 40, "Financial Request"),
        ("no experience", 20, "Unrealistic Pay"),
        ("hired instantly", 15, "Extreme Urgency")
      ]

    for word, weight, label in scam_keywords:
        if word in job_text:
            score += weight
            breakdown.append({"label": label, "pts": -weight})

    final_score = min(score, 100)
    
    # 3. Verdict Categorization
    if final_score >= 70:
        verdict = "Scam"
        color = "rose"
    elif final_score >= 30:
        verdict = "Suspicious"
        color = "amber"
    else:
        verdict = "Likely Safe"
        color = "emerald"

    return jsonify({
        "verdict": verdict,
        "color": color,
        "score": final_score,
        "breakdown": breakdown,
        "verify_flags": verify_flags,
        "explanation": "Dangerous activity detected." if final_score >= 70 else "Proceed with caution."
    })

if __name__ == '__main__':
    app.run(debug=True)
