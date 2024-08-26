from email.mime.text import MIMEText
from smtplib import SMTP, SMTPException
from app.config import settings

def send_verification_email(email: str, verification_link: str):
    msg = MIMEText(f"Please verify your email by clicking on the following link: {verification_link}")
    msg['Subject'] = 'Verify your email'
    msg['From'] = settings.smtp_user
    msg['To'] = email

    try:
        with SMTP(settings.smtp_server, settings.smtp_port) as server:
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(msg)
    except SMTPException as e:
        # Log the exception or handle it accordingly
        print(f"Failed to send email: {e}")
