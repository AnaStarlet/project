import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email_storage import save_email

MAILHOG_HOST = os.getenv("MAILHOG_HOST", "mailhog")
MAILHOG_PORT = int(os.getenv("MAILHOG_PORT", 1025))

def send_verification_email(to_email: str, username: str, token: str):
    try:
        msg = MIMEMultipart()
        msg['From'] = "noreply@notes-app.com"
        msg['To'] = to_email
        msg['Subject'] = "Подтверждение email для Notes App"

        verification_link = f"http://localhost:5173/verify-email?token={token}"
        body = f"""
        <html>
            <body>
                <h1>Добро пожаловать в Notes App, {username}!</h1>
                <p>Подтвердите email: <a href="{verification_link}">Ссылка</a></p>
                <p>Ссылка действительна 24 часа.</p>
            </body>
        </html>
        """

        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(MAILHOG_HOST, MAILHOG_PORT) as server:
            server.send_message(msg)

        save_email({
            "to": to_email,
            "subject": "Подтверждение email для Notes App",
            "html": body
        })

        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_password_reset_email(to_email: str, username: str, reset_token: str):
    try:
        msg = MIMEMultipart()
        msg['From'] = "noreply@notes-app.com"
        msg['To'] = to_email
        msg['Subject'] = "Сброс пароля для Notes App"

        reset_link = f"http://localhost:5173/reset-password?token={reset_token}"
        body = f"""
        <html>
            <body>
                <h1>Сброс пароля для {username}</h1>
                <p>Перейдите по ссылке: <a href="{reset_link}">Сбросить пароль</a></p>
                <p>Ссылка действительна 1 час.</p>
            </body>
        </html>
        """

        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(MAILHOG_HOST, MAILHOG_PORT) as server:
            server.send_message(msg)

        save_email({
            "to": to_email,
            "subject": "Сброс пароля для Notes App",
            "html": body
        })

        return True
    except Exception as e:
        print(f"Error sending password reset email: {e}")
        return False