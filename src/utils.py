import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config import Config

def send_email_to_mailhog(to_email, subject, html_body):
    message = MIMEMultipart()
    message["From"] = Config.SENDER_EMAIL
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(Config.SMTP_HOST, Config.SMTP_PORT) as server:
            server.sendmail(Config.SENDER_EMAIL, [to_email], message.as_string())
        return True
    except:
        return False