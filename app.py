from flask import Flask, render_template, request, jsonify, redirect, session
import pickle
import re
import os
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "smartsms_secret_key"

# Load Model
model      = pickle.load(open("models/classifier.pkl", "rb"))
vectorizer = pickle.load(open("models/vectorizer.pkl", "rb"))

# ── User Helpers ──────────────────────────────────────────────────────────────
def load_users():
    if not os.path.exists("users.json"):
        return {}
    with open("users.json", "r") as f:
        return json.load(f)

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

# ── Text Cleaning ─────────────────────────────────────────────────────────────
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    return text

# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("home.html", user=session["user"])

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        users = load_users()
        if username in users and check_password_hash(users[username], password):
            session["user"] = username
            return redirect("/")
        error = "Invalid username or password."
    return render_template("login.html", error=error)

@app.route("/register", methods=["GET", "POST"])
def register():
    error = None
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]
        if not username or not password:
            error = "Username and password required."
        else:
            users = load_users()
            if username in users:
                error = "User already exists."
            else:
                users[username] = generate_password_hash(password)
                save_users(users)
                return redirect("/login")
    return render_template("register.html", error=error)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

@app.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return jsonify({"error": "Not logged in"}), 401

    data = request.get_json()
    message = data.get("message", "")

    if not message.strip():
        return jsonify({"error": "Empty message"}), 400

    cleaned    = clean_text(message)
    vec        = vectorizer.transform([cleaned])
    prediction = model.predict(vec)[0]
    probability = model.predict_proba(vec)[0]
    spam_score = round(float(probability[1]) * 100, 2)

    return jsonify({
        "prediction": "Spam" if prediction == 1 else "Ham",
        "spam_probability": spam_score
    })

if __name__ == "__main__":
    app.run(debug=True)