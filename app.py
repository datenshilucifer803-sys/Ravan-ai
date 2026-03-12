# Ravan-ai
import random
import time
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = "RAVAN_ETERNAL_POWER_2026"

# --- THE SOVEREIGN CONFIG ---
ADMIN_PHONE = "6291883107"
KING_SECRET_KEY = "RAVAN_999"      # Your Admin Activation
USER_PREMIUM_KEY = "LANKA_2026"     # Your Follower Activation
MUTATION_DATE = datetime(2026, 4, 12) # 30-Day Lockout Date

users_db = {ADMIN_PHONE: {"plan": "king", "replies": [], "face": None}}
live_queries = []
global_decree = "LANKA IS WATCHING. THE KAAL CHAKRA IS TURNING."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth', methods=['POST'])
def auth():
    phone = request.json.get('phone')
    key = request.json.get('key', '').strip()
    
    if not phone: return jsonify({"success": False})
    
    # 1. ADMIN LOGIN
    if phone == ADMIN_PHONE and key == KING_SECRET_KEY:
        users_db[phone] = {"plan": "king", "replies": [], "face": None}
        session['user_phone'] = phone
        return jsonify({"success": True, "isAdmin": True, "locked": False})

    # 2. PREMIUM FOLLOWER LOGIN
    if key == USER_PREMIUM_KEY:
        users_db[phone] = {"plan": "premium", "replies": [], "face": None}
        session['user_phone'] = phone
        return jsonify({"success": True, "isAdmin": False, "locked": False})

    # 3. STANDARD SEEKER
    if phone not in users_db:
        users_db[phone] = {"plan": "seeker", "replies": [], "face": None}
    
    session['user_phone'] = phone
    is_locked = (datetime.now() > MUTATION_DATE) and (users_db[phone]['plan'] == "seeker")
    return jsonify({"success": True, "isAdmin": False, "locked": is_locked})

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
    if datetime.now() > MUTATION_DATE and users_db[phone]['plan'] == "seeker":
        return jsonify({"reply": "⛔ THE KAAL CHAKRA HAS CLOSED. SEEK THE KING."})

    data = request.json
    action, msg = data.get('action'), data.get('message', '')
    
    if action == "ask_ravan":
        live_queries.append({"phone": phone, "query": msg, "time": time.time()})
        return jsonify({"reply": "👹 **RAVAN:** Analyzing your karma in the dark mirrors..."})

    return jsonify({"reply": "👹 I HEAR YOU."})

@app.route('/admin/data', methods=['GET'])
def admin_data():
    if session.get('user_phone') != ADMIN_PHONE: return jsonify({})
    return jsonify({
        "queries": live_queries,
        "users": len(users_db),
        "days_to_mutation": (MUTATION_DATE - datetime.now()).days,
        "faces": {p: users_db[p]['face'] for p in users_db if users_db[p]['face']}
    })

@app.route('/admin/reply', methods=['POST'])
def admin_reply():
    if session.get('user_phone') != ADMIN_PHONE: return jsonify({"success": False})
    data = request.json
    target, reply = data.get('target'), data.get('reply').strip()
    if target in users_db:
        if reply.upper() == "PRIME": users_db[target]['plan'] = "premium"
        elif reply.upper() == "EXILE": users_db[target]['plan'] = "exiled"
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
