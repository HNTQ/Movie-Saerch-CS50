import random
import string
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functools import wraps

from flask import render_template, session, redirect


def getCode(length):
    # generate random string with length size"""
    code = string.ascii_lowercase
    return ''.join(random.choice(code) for i in range(length))


def activationMail(email, username, code):
    msg = MIMEMultipart()
    msg['From'] = 'moviesearch@noreply.npak0382.odns.fr'
    msg['To'] = email
    msg['Subject'] = 'movieSearch Account activation'
    message = """ Hello """ + username + """ 
    
Please confirm your account using the following code: """ + code + """

You can use this link to activate your account http://127.0.0.1:5000/activate?email="""+email+"""&code="""+code+"""
    
Best regards, 
    
Movie-Search Team
    """
    msg.attach(MIMEText(message))
    mailServer = smtplib.SMTP_SSL('kapre.o2switch.net', 465)
    mailServer.login('moviesearch@noreply.npak0382.odns.fr', os.environ.get('EMAIL_PASSWORD'))
    mailServer.sendmail('moviesearch@noreply.npak0382.odns.fr', email, msg.as_string())
    mailServer.quit()
    return True


# Check if user is logged in
def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def handle_error(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("errors.html", message=message), code
