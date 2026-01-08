import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, jsonify

app = Flask(__name__)

# 🔐 Load Firebase key from Render ENV
firebase_key = os.environ.get("FIREBASE_KEY_JSON")

if not firebase_key:
    raise Exception("FIREBASE_KEY_JSON not found in environment")

cred_dict = json.loads(firebase_key)
cred = credentials.Certificate(cred_dict)

firebase_admin.initialize_app(cred)

db = firestore.client()

@app.route("/")
def home():
    return "DealNawabi QR Backend is running 🚀"

@app.route("/health")
def health():
    return jsonify({"status": "OK"})