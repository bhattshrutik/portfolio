import traceback
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory,jsonify
from flask_mail import Mail, Message

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Required for flash messages

# Flask-Mail Configuration using .env variables
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']
app.config['MAIL_RECEIVER'] = os.getenv('MAIL_RECEIVER')

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

import traceback  # Import for debugging

@app.route('/submit', methods=['POST'])
def submit():
    try:
        email = request.form.get('email')
        message_body = request.form.get('message')

        if not email or not message_body:
            return jsonify({"status": "error", "message": "Email and message are required!"}), 400

        msg = Message("New Contact Form Submission", recipients=[app.config['MAIL_RECEIVER']])
        msg.body = f"From: {email}\n\n{message_body}"
        mail.send(msg)

        return jsonify({"status": "success", "message": "Message sent successfully!"}), 200

    except Exception as e:
        print(f"Error: {e}")  # Debugging
        return jsonify({"status": "error", "message": "An error occurred. Please try again."}), 500


# Serve profile image and resume from the root directory
@app.route('/<filename>')
def serve_file(filename):
    return send_from_directory(os.getcwd(), filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
