from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

# Flask-Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'bhattshrutik36@gmail.com'  # Replace with your email
app.config['MAIL_PASSWORD'] = 'iowb haof cqho ouvw'  # Replace with your app password
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']
app.config['MAIL_RECEIVER'] = 'bhattshrutik36@gmail.com'  # Replace with receiver email

mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form.get('email')
    message_body = request.form.get('message')

    if email and message_body:
        msg = Message("New Contact Form Submission", recipients=[app.config['MAIL_RECEIVER']])
        msg.body = f"From: {email}\n\n{message_body}"
        mail.send(msg)
    
    return redirect(url_for('index'))  # Redirect back to home page

if __name__ == '__main__':
    app.run(debug=True, port=5000)
