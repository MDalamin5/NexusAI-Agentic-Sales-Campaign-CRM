import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_mailhog():
    # 1. Setup details
    smtp_host = "localhost"
    smtp_port = 1025  # MailHog SMTP port
    sender_email = "ai-agent@gtr.com"
    receiver_email = "target-lead@elonmusk.com" # Can be anything!

    # 2. Create the message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Personalized Outreach Test"

    body = "Hello! This is a test email caught by MailHog."
    message.attach(MIMEText(body, "plain"))

    # 3. Send the mail
    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("✅ Success! Check http://localhost:8025")
    except Exception as e:
        print(f"❌ Failed to send: {e}")

if __name__ == "__main__":
    test_mailhog()