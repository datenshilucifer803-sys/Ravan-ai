# Ravan-ai
from flask import Flask, render_template, request, jsonify, session
import os

app = Flask(__name__)
app.secret_key = "RAVAN_POWER_SECRET"

# --- ADMIN & KEYS ---
ADMIN_PHONE = "6291883107"
MASTER_CODE = "RAVAN_SUPREME_2026"
# These are the 10 keys you can sell
VALID_KEYS = ["LANKA2026", "RAVAN_KING_99", "MAYAVI_SHAKTI", "DASHANAN_VIP", "GOLDEN_CITY_7", "TANDAV_POWER", "RAHU_KAAL_X", "AMRIT_KUND", "VEDA_SECRET", "MYSTIC_ADMIN_1"]

# Database Simulation
users_db = {
    "6291883107": {"plan": "premium_plus", "status": "King"}
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth', methods=['POST'])
def auth():
    data = request.json
    phone = data.get('phone')
    if phone not in users_db:
        users_db[phone] = {"plan": "free", "status": "Seeker"}
    session['user_phone'] = phone
    return jsonify({"success": True, "plan": users_db[phone]['plan']})

@app.route('/activate', methods=['POST'])
def activate():
    key = request.json.get('key', '').upper()
    phone = session.get('user_phone')
    if not phone: return jsonify({"success": False, "msg": "Login first!"})

    if key == MASTER_CODE or key in VALID_KEYS:
        users_db[phone]['plan'] = "premium_plus"
        return jsonify({"success": True, "msg": "👹 PREMIUM UNLOCKED. DARK SECRETS REVEALED."})
    return jsonify({"success": False, "msg": "INVALID TRIBUTE. KEY REJECTED."})

@app.route('/god_eye', methods=['GET'])
def god_eye():
    if session.get('user_phone') != ADMIN_PHONE:
        return jsonify({"success": False, "msg": "Access Denied!"})
    return jsonify({"success": True, "users": users_db})

@app.route('/process', methods=['POST'])
def process():
    phone = session.get('user_phone')
    data = request.json
    action = data.get('action')
    is_premium = users_db.get(phone, {}).get('plan') == "premium_plus"

    if action == "black_magic" and not is_premium:
        return jsonify({"reply": "⛔ LOCKED. This requires Premium Plus. Pay ₹299 to 6291883107@fam and send screenshot to WhatsApp."})

    responses = {
        "kundli": "📜 RAVAN: Your birth chart shows a strong influence of Saturn. Success comes through discipline.",
        "zodiac": "♈ RAVAN: The stars suggest you avoid new investments today. Meditate on the Sun.",
        "black_magic": "💀 EXTREME TOTKA: To remove bad luck, throw a handful of black sesame seeds over your left shoulder at a crossroads."
    }
    return jsonify({"reply": responses.get(action, "👹 RAVAN: I am listening to your soul.")})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
