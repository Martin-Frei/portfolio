import requests
from django.shortcuts import render
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from projects.models import Project
from .models import Profile


def home(request):
    profile = Profile.objects.first()
    featured_projects = Project.objects.filter(is_public_demo=True)[:2]
    return render(
        request,
        "core/home.html",
        {"profile": profile, "featured_projects": featured_projects},
    )


def about(request):
    profile = Profile.objects.first()
    return render(request, "core/about.html", {"profile": profile})


def contact(request):
    profile = Profile.objects.first()
    return render(request, "core/contact.html", {"profile": profile})


def skills(request):
    return render(request, "core/skills.html")


import requests  # WICHTIG: Oben hinzufügen!
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render


def contact(request):
    if request.method == "POST":
        # Formulardaten holen
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        company = request.POST.get("company", "").strip()
        subject = request.POST.get("subject", "").strip()
        message_text = request.POST.get("message", "").strip()

        # Validation
        if not all([name, email, subject, message_text]):
            messages.error(request, "❌ Bitte fülle alle Pflichtfelder aus!")
            return render(request, "core/contact.html")

        # Deine schönen Texte (bleiben exakt gleich)
        email_body_to_you = f"""
🔔 Neue Kontaktanfrage über dein Portfolio!

Von: {name}
Email: {email}
Unternehmen: {company or 'Nicht angegeben'}
Betreff: {subject}

Nachricht:
{message_text}

---
💡 TIPP: Einfach auf diese Email ANTWORTEN um {name} direkt zu kontaktieren!
Die Antwort geht automatisch an: {email}
        """

        confirmation_body = f"""
Hallo {name},

vielen Dank für deine Nachricht! 🎉

Ich habe deine Anfrage erhalten und melde mich so schnell wie möglich bei dir – in der Regel innerhalb von 24 Stunden.

Hier nochmal deine Nachricht zur Sicherheit:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Betreff: {subject}

{message_text}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Falls du noch etwas ergänzen möchtest, antworte einfach auf diese Email!

Beste Grüße,
Martin Freimuth
Fullstack Developer
        """

        # --- AB HIER DIE NEUE LOGIK (API statt SMTP) ---
        resend_url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {settings.RESEND_API_KEY}",
            "Content-Type": "application/json",
        }

        try:
            # 1. Email an DICH
            payload_to_me = {
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": "mat.frei@gmx.de",
                "subject": f"📬 Kontaktanfrage: {subject}",
                "reply_to": email,
                "text": email_body_to_you,
            }
            resp_me = requests.post(
                resend_url, headers=headers, json=payload_to_me, timeout=10
            )

            if resp_me.status_code == 201:
                # 2. Bestätigung an USER (nur wenn die erste Mail geklappt hat)
                payload_to_user = {
                    "from": settings.DEFAULT_FROM_EMAIL,
                    "to": email,
                    "subject": "✅ Deine Nachricht an Martin Freimuth wurde empfangen",
                    "reply_to": "mat.frei@gmx.de",
                    "text": confirmation_body,
                }
                requests.post(
                    resend_url, headers=headers, json=payload_to_user, timeout=10
                )

                messages.success(request, "✅ Nachricht erfolgreich versendet!")
            else:
                print(f"Resend API Error: {resp_me.text}")
                messages.error(request, "❌ Resend Fehler: " + resp_me.text)

        except Exception as e:
            print(f"API Connection Error: {e}")
            messages.error(request, "❌ Verbindung zu Resend fehlgeschlagen (Timeout).")

    return render(request, "core/contact.html")
