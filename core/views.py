from django.shortcuts import render
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings

def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def skills(request):
    return render(request, 'core/skills.html')

def contact(request):
    if request.method == 'POST':
        # Formulardaten holen
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        company = request.POST.get('company', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()
        
        # Validation
        if not all([name, email, subject, message_text]):
            messages.error(request, '❌ Bitte fülle alle Pflichtfelder aus!')
            return render(request, 'core/contact.html')
        
        # Email-Text für DICH zusammenbauen
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
        
        # Bestätigungs-Email für USER
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

🌐 https://martin-freimuth.dev
💼 LinkedIn: https://www.linkedin.com/in/martin-freimuth-089249359/
🐙 GitHub:   https://github.com/Martin-Frei

---
Diese Email wurde an {email} gesendet.
Falls du diese Nachricht nicht erwartet hast, kannst du sie einfach ignorieren.
        """
        
        try:
            # 1. Email an DICH mit Reply-To auf User
            email_to_you = EmailMessage(
                subject=f'📬 Kontaktanfrage: {subject}',
                body=email_body_to_you,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=['mat.frei@gmx.de'],
                reply_to=[email],  # User kann direkt erreicht werden!
            )
            email_to_you.send()
            
            # 2. Bestätigung an USER mit Reply-To auf dich
            try:
                confirmation = EmailMessage(
                    subject=f'✅ Deine Nachricht an Martin Freimuth wurde empfangen',
                    body=confirmation_body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[email],
                    reply_to=['mat.frei@gmx.de'],  # User kann dir antworten!
                )
                confirmation.send()
                
                messages.success(
                    request, 
                    '✅ Nachricht erfolgreich versendet! Du erhältst eine Bestätigungs-Email (check auch deinen Spam-Ordner).'
                )
            except Exception as e:
                # Bestätigung fehlgeschlagen? Nicht dramatisch!
                messages.success(
                    request,
                    '✅ Nachricht wurde versendet! Bestätigungs-Email konnte nicht zugestellt werden (bitte Email-Adresse prüfen).'
                )
                print(f"Confirmation email failed: {e}")  # Für Logs
            
        except Exception as e:
            messages.error(
                request, 
                f'❌ Fehler beim Versenden! Bitte versuche es später nochmal oder kontaktiere mich direkt per Email.'
            )
            print(f"Contact form error: {e}")  # Für Logs
    
    return render(request, 'core/contact.html')