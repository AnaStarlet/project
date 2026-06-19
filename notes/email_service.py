import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
import logging

logger = logging.getLogger(__name__)

MAIL_HOST = os.getenv("MAIL_HOST", "localhost")
MAIL_PORT = int(os.getenv("MAIL_PORT", 1025))
MAIL_USER = os.getenv("MAIL_USER", "")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD", "")
MAIL_USE_TLS = os.getenv("MAIL_USE_TLS", "false").lower() == "true"
MAIL_FROM = os.getenv("MAIL_FROM", "noreply@notes-app.com")

VERIFICATION_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Подтверждение регистрации</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; padding: 20px;">
    <h2 style="color: #007bff;">Здравствуйте, {{ username }}!</h2>
    <p>Спасибо за регистрацию в Notes App. Пожалуйста, подтвердите ваш адрес электронной почты, перейдя по ссылке ниже:</p>
    <p style="margin: 30px 0;">
        <a href="{{ verification_url }}" style="background-color: #007bff; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; font-weight: bold;">
            Подтвердить Email
        </a>
    </p>
    <p>Если кнопка выше не работает, скопируйте и вставьте следующую ссылку в адресную строку браузера:</p>
    <p><a href="{{ verification_url }}" style="color: #007bff;">{{ verification_url }}</a></p>
    <hr style="border: none; border-top: 1px solid #eee; margin-top: 30px;">
    <p style="font-size: 12px; color: #777;">Если вы не регистрировались в нашем приложении, просто проигнорируйте это письмо.</p>
</body>
</html>
"""

RESET_PASSWORD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Сброс пароля</title>
</head>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; padding: 20px;">
    <h2 style="color: #28a745;">Здравствуйте, {{ username }}!</h2>
    <p>Вы получили это письмо, потому что для вашей учетной записи был отправлен запрос на сброс пароля.</p>
    <p style="margin: 30px 0;">
        <a href="{{ reset_url }}" style="background-color: #28a745; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block; font-weight: bold;">
            Сбросить пароль
        </a>
    </p>
    <p>If the button doesn't work, copy and paste this URL into your browser:</p>
    <p><a href="{{ reset_url }}" style="color: #28a745;">{{ reset_url }}</a></p>
    <hr style="border: none; border-top: 1px solid #eee; margin-top: 30px;">
    <p style="font-size: 12px; color: #777;">Если вы не запрашивали сброс пароля, просто проигнорируйте это письмо.</p>
</body>
</html>
"""


def send_verification_email(to_email: str, username: str, verification_token: str):
    subject = "Подтверждение email для Notes App"
    template = Template(VERIFICATION_EMAIL_TEMPLATE)
    verification_url = f"http://localhost:8888/auth/verify?token={verification_token}"

    print("\n" + "="*80)
    print(" ССЫЛКА ДЛЯ ПОДТВЕРЖДЕНИЯ РЕГИСТРАЦИИ (СКОПИРУЙТЕ ЕЁ В БРАУЗЕР):")
    print(f" {verification_url}")
    print("="*80 + "\n")

    html_content = template.render(
        username=username,
        verification_url=verification_url
    )

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = MAIL_FROM
    msg["To"] = to_email

    part = MIMEText(html_content, "html")
    msg.attach(part)

    try:
        with smtplib.SMTP(MAIL_HOST, MAIL_PORT) as server:
            if MAIL_USE_TLS:
                server.starttls()
            if MAIL_USER and MAIL_PASSWORD:
                server.login(MAIL_USER, MAIL_PASSWORD)

            server.sendmail(MAIL_FROM, to_email, msg.as_string())

        logger.info(f"Verification email sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False


def send_password_reset_email(to_email: str, username: str, reset_token: str):
    subject = "Сброс пароля Notes App"
    template = Template(RESET_PASSWORD_TEMPLATE)
    reset_url = f"http://localhost:8888/auth/reset-password?token={reset_token}"

    print("\n" + "="*80)
    print(" ССЫЛКА ДЛЯ СБРОСА ПАРОЛЯ:")