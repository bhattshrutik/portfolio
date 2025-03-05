import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message

# Load environment variables
load_dotenv()

app = Flask(__name__)

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
    return open('index.html').read()

@app.route('/submit', methods=['POST'])
def submit():
    try:
        email = request.form.get('email')
        message_body = request.form.get('message')

        if not email or not message_body:
            return redirect(url_for('index'))  # Redirect if form is empty

        msg = Message("New Contact Form Submission", recipients=[app.config['MAIL_RECEIVER']])
        msg.body = f"From: {email}\n\n{message_body}"
        mail.send(msg)

        print("Email sent successfully")  # Debugging

        return redirect(url_for('index'))  # Redirect to the home page

    except Exception as e:
        print(f"Error: {e}")  # Print actual error
        return "An error occurred. Please try again later.", 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
