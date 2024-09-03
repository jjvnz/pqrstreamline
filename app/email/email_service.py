from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTPException
from fastapi import HTTPException
from app.config import settings
import logging
from urllib.parse import urlencode

logger = logging.getLogger(__name__)

def send_verification_email(email: str, token: str):
    verification_link = f"{settings.base_url}/auth/verify?{urlencode({'email': email, 'token': token, 'mode': 'signup'})}"

    subject = 'Complete Your Signup for Our Service'
    body = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
                color: #333;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 0 auto;
                background-color: #ffffff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                overflow: hidden;
            }}
            .header {{
                background-color: #007bff;
                color: #ffffff;
                padding: 20px;
                text-align: center;
            }}
            .content {{
                padding: 20px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 24px;
                margin: 20px 0;
                background-color: #007bff;
                color: #ffffff;
                text-decoration: none;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }}
            .footer {{
                background-color: #f4f4f4;
                padding: 10px;
                text-align: center;
                font-size: 14px;
            }}
            a {{
                color: #007bff;
                text-decoration: none;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to Our Service!</h1>
            </div>
            <div class="content">
                <p>We have received a signup attempt from your email address. To complete the signup process, please click the button below:</p>
                <p><a href="{verification_link}" class="button">VERIFY</a></p>
                <p>Or copy and paste this URL into a new tab of your browser:</p>
                <p><a href="{verification_link}">{verification_link}</a></p>
                <p>Please note that by completing your signup you are agreeing to our <a href="{settings.terms_url}">Terms of Service</a> and <a href="{settings.privacy_url}">Privacy Policy</a>.</p>
            </div>
            <div class="footer">
                <p>Thank you for choosing our service.</p>
            </div>
        </div>
    </body>
    </html>
    """

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = settings.smtp_user
    msg['To'] = email
    msg.attach(MIMEText(body, 'html'))

    try:
        with SMTP(settings.smtp_server, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(msg)
    except SMTPException as e:
        logger.error(f"Failed to send email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send verification email")
