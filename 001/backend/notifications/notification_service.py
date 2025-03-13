from typing import List, Dict, Optional
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import firebase_admin
from firebase_admin import messaging
import os

class NotificationService:
    def __init__(self):
        self.email_config = {
            "hostname": os.getenv("SMTP_HOST"),
            "port": int(os.getenv("SMTP_PORT")),
            "username": os.getenv("SMTP_USER"),
            "password": os.getenv("SMTP_PASS")
        }
        
        # Initialisation Firebase pour les notifications push
        cred = firebase_admin.credentials.Certificate(
            os.getenv("FIREBASE_ADMIN_SDK_PATH")
        )
        firebase_admin.initialize_app(cred)

    async def send_email(
        self,
        to_email: str,
        subject: str,
        content: str,
        template_id: Optional[str] = None
    ):
        """Envoi d'email"""
        message = MIMEMultipart()
        message["From"] = "Deep Study AI <noreply@deepstudy.ai>"
        message["To"] = to_email
        message["Subject"] = subject
        
        if template_id:
            content = await self._get_email_template(template_id, content)
            
        message.attach(MIMEText(content, "html"))
        
        async with aiosmtplib.SMTP(**self.email_config) as smtp:
            await smtp.send_message(message)

    async def send_push_notification(
        self,
        user_id: str,
        title: str,
        body: str,
        data: Optional[Dict] = None
    ):
        """Envoi de notification push"""
        # Récupération du token Firebase du user
        user_tokens = await self._get_user_fcm_tokens(user_id)
        
        for token in user_tokens:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data,
                token=token
            )
            
            try:
                messaging.send(message)
            except Exception as e:
                await self._handle_invalid_token(user_id, token) 