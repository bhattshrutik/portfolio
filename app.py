import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')  # Set secret key from GitHub Secrets

# Flask-Mail Configuration using GitHub Secrets
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))  # Default to 587 if not set
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']
app.config['MAIL_RECEIVER'] = os.getenv('MAIL_RECEIVER')

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        email = request.form.get('email')
        message_body = request.form.get('message')

        if not email or not message_body:
            flash("Email and message are required!", "error")
            return redirect(url_for('index'))

        msg = Message("New Contact Form Submission", recipients=[app.config['MAIL_RECEIVER']])
        msg.body = f"From: {email}\n\n{message_body}"
        mail.send(msg)

        flash("Your message has been sent successfully!", "success")
        return redirect(url_for('index'))

    except Exception as e:
        print(f"Error: {e}")  # Debugging
        flash("An error occurred. Please try again later.", "error")
        return redirect(url_for('index'))

@app.route('/<filename>')
def serve_file(filename):
    return send_from_directory(os.getcwd(), filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
