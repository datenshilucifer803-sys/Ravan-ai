# Ravan-ai
import random
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = "RAVAN_SUPREME_2026"

ADMIN_PHONE = "6291883107"
KING_SECRET_KEY = "RAVAN_999"
USER_PREMIUM_KEY = "LANKA_2026"
MUTATION_DATE = datetime(2026, 4, 12)

users_db = {ADMIN_PHONE: {"plan": "king", "replies": [], "face": None}}
live_queries = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth', methods=['POST'])
def auth():
    phone = request.json.get('phone')
    key = request.json.get('key', '').strip()
    is_admin = (phone == ADMIN_PHONE and key == KING_SECRET_KEY)
    
    if phone not in users_db:
        users_db[phone] = {"plan": "premium" if key == USER_PREMIUM_KEY else "seeker", "replies": [], "face": None}
    
    session['user_phone'] = phone
    is_locked = (datetime.now() > MUTATION_DATE) and (users_db[phone]['plan'] == "seeker")
    return jsonify({"success": True, "isAdmin": is_admin, "locked": is_locked})

@app.route('/process', methods=['POST'])
def process():
    phone = session.get('user_phone')
    if not phone: return jsonify({"reply": "Unauthorized."})
    
    data = request.json
    action = data.get('action')
    
    # --- LIVE KUNDLI LOGIC ---
    if action == "kundli":
        power = random.randint(70, 99)
        return jsonify({"reply": f"📜 **LIVE KUNDLI (March 2026):**<br>• Strength: $P = {power}\%$<br>• Gana: Rakshasa<br>• Nadi: Antya<br>• Verdict: **SUPREME ASCENSION**"})

    # --- LIVE ZODIAC LOGIC ---
    if action == "zodiac":
        signs = ["Aries", "Leo", "Scorpio"]
        return jsonify({"reply": f"♈ **ASTRAL ALIGNMENT:**<br>The Sun is in {random.choice(signs)}.<br>Your current energy frequency is **High**. Avoid iron objects today."})

    if action == "ask_ravan":
        live_queries.append({"phone": phone, "query": data.get('message'), "time": time.time()})
        return jsonify({"reply": "👹 **RAVAN:** Your query is being weighed in the scales of Lanka."})

    return jsonify({"reply": "👹 I AM WATCHING."})

@app.route('/admin/data', methods=['GET'])
def admin_data():
    if session.get('user_phone') != ADMIN_PHONE: return jsonify({})
    return jsonify({
        "queries": live_queries,
        "users": len(users_db),
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
    res = {"has_reply": False}
    if phone in users_db and users_db[phone]["replies"]:
        res["has_reply"], res["reply"] = True, users_db[phone]["replies"].pop(0)
    return jsonify(res)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
        
