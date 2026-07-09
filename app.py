from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import requests
import smtplib
from flask_cors import CORS
from email.message import EmailMessage

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


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
        msg = EmailMessage()
        msg["Subject"] = "Thank You for Contacting Insha Traders"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = email

        msg.set_content(
            f"""
Hello {name},

Thank you for contacting Insha Traders.

We have received your inquiry and our team will contact you shortly.

Regards,
Insha Traders
"""
        )

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)

    except Exception as e:
        print(e)

    return jsonify({"success": True})


@app.route("/")
def home():
    return "Insha Traders Backend Running"


if __name__ == "__main__":
    app.run(debug=True)