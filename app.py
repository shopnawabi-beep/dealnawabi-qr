from flask import Flask, request, render_template_string
import firebase_admin
from firebase_admin import credentials, firestore

app = Flask(__name__)

# Initialize Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# HTML templates
activation_html = """
<!DOCTYPE html>
<html>
<head><title>Activate QR</title></head>
<body>
<h2>Activate Your QR Code</h2>
<form method="post">
  Enter Mobile Number:<br>
  <input type="text" name="mobile" required><br><br>
  <input type="submit" value="Activate">
</form>
</body>
</html>
"""

emergency_html = """
<!DOCTYPE html>
<html>
<head><title>Emergency Page</title></head>
<body>
<h2>Emergency Contact</h2>
<p><strong>Owner Mobile:</strong> {{ mobile }}</p>
<p>
  <a href="tel:{{ mobile }}"><button>Call Owner</button></a>
</p>
<p>
  <a href="tel:100"><button>Call Police</button></a>
</p>
<p>
  <a href="tel:102"><button>Call Ambulance</button></a>
</p>
</body>
</html>
"""

@app.route("/e/<qr_id>", methods=["GET", "POST"])
def handle_qr(qr_id):
    doc_ref = db.collection("qr_codes").document(qr_id)
    doc = doc_ref.get()

    if not doc.exists:
        return "Invalid QR Code", 404

    data = doc.to_dict()

    # If QR is unused → show activation page
    if data["status"] == "unused":
        if request.method == "POST":
            mobile = request.form["mobile"]
            doc_ref.update({
                "owner_mobile": mobile,
                "status": "active"
            })
            return f"QR Activated Successfully! Mobile saved: {mobile}"
        return render_template_string(activation_html)

    # If QR is active → show emergency page
    if data["status"] == "active":
        return render_template_string(emergency_html, mobile=data["owner_mobile"])

    return "Invalid QR Status", 403


if __name__ == "__main__":
    app.run(debug=True)
