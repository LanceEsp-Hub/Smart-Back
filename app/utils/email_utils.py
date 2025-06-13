#backend\app\utils\email_utils.py

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from pydantic import BaseModel, EmailStr
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file


print("MAIL_USERNAME:", os.getenv("MAIL_USERNAME"))
print("MAIL_PASSWORD:", os.getenv("MAIL_PASSWORD"))
print("MAIL_FROM:", os.getenv("MAIL_FROM"))
print("MAIL_PORT:", os.getenv("MAIL_PORT"))
print("MAIL_SERVER:", os.getenv("MAIL_SERVER"))

class EmailSchema(BaseModel):
    email: EmailStr

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,  # Correct key
    MAIL_SSL_TLS=False,  # Correct key
    USE_CREDENTIALS=True
)

async def send_verification_email(email: str, token: str):
    verification_url = f"http://127.0.0.1:8000/api/verify-email?token={token}"

    message = MessageSchema(
        subject="Email Verification",
        recipients=[email],
        body=f"Click the link to verify your email: {verification_url}",
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_password_reset_email(email: str, reset_token: str):
    reset_url = f"http://localhost:3000/reset-password?token={reset_token}"

    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email],
        body=f"Click the link to reset your password: {reset_url}",
        subtype="html",
    )

    fm = FastMail(conf)
    await fm.send_message(message)