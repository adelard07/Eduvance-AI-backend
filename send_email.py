import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dataclasses import dataclass
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv("config.env")

@dataclass
class SendMessage:
    sender_name: str
    sender_email: str
    sender_subject: str
    sender_message: str

    # Load SMTP credentials securely
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", 587))
    _email: str = os.getenv("ADELARD_USER_EMAIL")
    _password: str = os.getenv("ADELARD_USER_PASSWORD")
    receiver_email: str = os.getenv("ADELARD_USER_EMAIL")

    def send_email(self):
        if not all([self._email, self._password, self.receiver_email]):
            logging.error("SMTP credentials are missing in environment variables.")
            return {"status": "error", "message": "SMTP credentials are missing."}

        try:
            # Connect to SMTP server
            logging.info(f"Connecting to SMTP server: {self.smtp_server}:{self.smtp_port}")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(self._email, self._password)

            # Create email content
            msg = MIMEMultipart()
            msg["From"] = f"{self.sender_name} <{self.sender_email}>"
            msg["To"] = self.receiver_email
            msg["Subject"] = self.sender_subject

            email_body = f"""From: {self.sender_name}
Email: {self.sender_email}
Subject: {self.sender_subject}
Message: {self.sender_message}
"""

            msg.attach(MIMEText(email_body.strip(), "plain"))

            # Send email
            logging.info(f"Sending email from {self._email} to {self.receiver_email}")
            server.sendmail(self._email, self.receiver_email, msg.as_string())
            server.quit()

            logging.info("Email sent successfully!")
            return {"status": "success", "message": "Email sent successfully."}

        except smtplib.SMTPAuthenticationError:
            logging.error("SMTP authentication failed. Check your email/password.")
            return {"status": "error", "message": "SMTP authentication failed. Check credentials."}

        except smtplib.SMTPException as e:
            logging.error(f"SMTP error: {e}")
            return {"status": "error", "message": f"SMTP error: {str(e)}"}

        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            return {"status": "error", "message": f"Unexpected error: {str(e)}"}

# Run the script for testing
if __name__ == "__main__":
    sender_name = "John Doe"
    sender_email = "johndoe@example.com"
    sender_subject = "Test Subject"
    sender_message = "This is a test email. Testing again"

    mail = SendMessage(
        sender_name=sender_name,
        sender_email=sender_email,
        sender_subject=sender_subject,
        sender_message=sender_message,
    )
    result = mail.send_email()
    print(result)
