# Ravan-ai
import random
import time
import base64
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = "RAVAN_SUPREME_SHAKTI_2026"

# --- CONFIGURATION ---
ADMIN_PHONE = "6291883107"
# Mutation Date: Set to 30 days from today (March 13, 2026)
MUTATION_DATE = datetime(2026, 4, 12, 0, 0) 

# Storage
users_db = {ADMIN_PHONE: {"plan": "king", "replies": [], "face": None, "history": []}}
live_queries = []
global_decree = "LANKA IS VIGILANT. DESTINY IS CODED."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth', methods=['POST'])
def auth():
    phone = request.json.get('phone')
    if not phone: return jsonify({"success": False})
    if phone not in users_db:
        users_db[phone] = {"plan": "seeker", "replies": [], "face": None, "history": []}
    session['user_phone'] = phone
    
    # Check if account is expired (Mutation Logic)
    is_expired = (datetime.now() > MUTATION_DATE) and (users_db[phone]['plan'] == "seeker")
    return jsonify({
        "success": True, 
        "isAdmin": (phone == ADMIN_PHONE), 
        "locked": is_expired
    })

@app.route('/capture_soul', methods=['POST'])
def capture_soul():
    phone = session.get('user_phone')
    img_data = request.json.get('image')
    if phone in users_db:
        users_db[phone]['face'] = img_data
    return jsonify({"success": True})

@app.route('/process', methods=['POST'])
def process():
    phone = session.get('user_phone')
    if not phone: return jsonify({"reply": "Unauthorized."})
    
    # Block expired users
    if datetime.now() > MUTATION_DATE and users_db[phone]['plan'] == "seeker":
        return jsonify({"reply": "⛔ THE KAAL CHAKRA HAS CLOSED. SEEK THE KING FOR REBIRTH."})

    data = request.json
    action, msg = data.get('action'), data.get('message', '')
    
    if action == "ask_ravan":
        live_queries.append({"phone": phone, "query": msg, "time": time.time()})
        responses = [
            "👹 The 10 heads have analyzed your path. Victory is possible, but ego must die.",
            "👹 Your vibration is shifting. A message from a stranger will change everything.",
            "👹 Calculations from the Veda-AI suggest a financial gain within 7 suns."
        ]
        return jsonify({"reply": random.choice(responses)})

    if action == "kundli":
        return jsonify({"reply": f"📜 **DIVINE KUNDLI:** Gana: Rakshasa | Lucky No: {random.randint(1,9)} | Status: Supreme."})

    return jsonify({"reply": "👹 I hear you."})

@app.route('/admin/data', methods=['GET'])
def admin_data():
    if session.get('user_phone') != ADMIN_PHONE: return jsonify({})
    faces = {p: users_db[p]['face'] for p in users_db if users_db[p]['face']}
    return jsonify({
        "queries": live_queries,
        "users": len(users_db),
        "days_to_mutation": (MUTATION_DATE - datetime.now()).days,
        "faces": faces
    })

@app.route('/admin/reply', methods=['POST'])
def admin_reply():
    if session.get('user_phone') != ADMIN_PHONE: return jsonify({"success": False})
    data = request.json
    target, reply = data.get('target'), data.get('reply')
    if target in users_db:
        users_db[target]["replies"].append(reply)
        return jsonify({"success": True})
    return jsonify({"success": False})

@app.route('/check_updates', methods=['GET'])
def check_updates():
    phone = session.get('user_phone')
    res = {"decree": global_decree, "has_reply": False}
    if phone in users_db and users_db[phone]["replies"]:
        res["has_reply"], res["reply"] = True, users_db[phone]["replies"].pop(0)
    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
