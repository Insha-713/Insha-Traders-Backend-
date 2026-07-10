from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests
from flask_cors import CORS
import resend
load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID") 

@app.route("/contact", methods=["POST"])
def contact():

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    phone = data.get("mobile")
    location = data.get("location")
    message = data.get("message")

    telegram_message = f"""
🔔 New Insha Traders Inquiry

👤 Name: {name}
📧 Email: {email}
📱 Mobile: {phone}
📍 Location: {location}

💬 Message:
{message}
"""

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": telegram_message
        }
    )
    try:
        resend.Emails.send({
            "from": "onboarding@resend.dev",
            "to": [email],
            "subject": "Thank You for Contacting Insha Traders",
            "html": f"""
            <h2>Thank You for Contacting Insha Traders</h2>

            <p>Dear {name},</p>

            <p>We have successfully received your inquiry.</p>

            <p>Our team will review your requirements and contact you shortly.</p>

            <p>For urgent assistance, please call us directly.</p>

            <p>Regards,<br>
            Insha Traders</p>
        
            """
        })
    except Exception as e:
        print("EMAIL ERROR:", e)
        return jsonify({"success": False, "error": str(e)}),500

    return jsonify({"success": True})


@app.route("/")
def home():
    return "Insha Traders Backend Running"


if __name__ == "__main__":
    app.run(debug=True)