"""
Custom Email Backend für Resend API
Nutzt API statt SMTP (schneller & zuverlässiger!)
"""
import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend


class ResendAPIBackend(BaseEmailBackend):
    """
    Sendet Emails via Resend API statt SMTP
    """
    
    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        
        sent_count = 0
        url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {settings.RESEND_API_KEY}",
            "Content-Type": "application/json",
        }
        
        for message in email_messages:
            payload = {
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": message.to,
                "subject": message.subject,
                "text": message.body,
            }
            
            if message.reply_to:
                payload["reply_to"] = message.reply_to[0]
            
            try:
                response = requests.post(url, headers=headers, json=payload, timeout=10)
                
                if response.ok:
                    sent_count += 1
                else:
                    if not self.fail_silently:
                        raise Exception(f"Resend API Error: {response.status_code}")
                    
            except Exception as e:
                if not self.fail_silently:
                    raise
        
        return sent_count