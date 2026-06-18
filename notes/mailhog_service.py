import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

MAILHOG_HOST = os.getenv("MAILHOG_HOST", "localhost")
MAILHOG_PORT = int(os.getenv("MAILHOG_PORT", 1025))

def send_verification_email(to_email: str, username: str, token: str):
    try:
        msg = MIMEMultipart()
        msg['From'] = "noreply@notes-app.com"
        msg['To'] = to_email
        msg['Subject'] = "Подтверждение email для Notes App"

        verification_link = f"http://localhost:5173/?token={token}"
        body = f"""
        <html>
            <body>
                <h1>Добро пожаловать в Notes App, {username}!</h1>
                <p>Подтвердите email: <a href="{verification_link}">Ссылка</a></p>
            </body>
        </html>
        """

        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(MAILHOG_HOST, MAILHOG_PORT) as server:
            server.send_message(msg)

        return True
    except Exception as e:
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
                <p><a href="{reset_link}">Сбросить пароль</a></p>
            </body>
        </html>
        """

        msg.attach(MIMEText(body, 'html'))

        with smtplib.SMTP(MAILHOG_HOST, MAILHOG_PORT) as server:
            server.send_message(msg)

        return True
    except Exception as e:
        return False