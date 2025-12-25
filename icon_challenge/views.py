"""
Icon-Challenge Views
HTMX Endpoints für Challenge-System
"""

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
import time

from .engine import IconChallengeEngine, cleanup_challenge
from .config import CHALLENGE_CONTEXTS

from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

import requests
from django.conf import settings


# ============================================
# 1. CHALLENGE STARTEN (Modal öffnen)
# ============================================


@require_GET
def start_challenge(request, context_type):
    """
    Starte neue Challenge - Zeige Modal

    URL: /icon-challenge/start/<context_type>/
    Context: 'guest', 'contact', 'signup'

    Returns:
        HTML: Modal mit 9 Icons
    """
    # 1. Validierung: Context existiert?
    if context_type not in CHALLENGE_CONTEXTS:
        return HttpResponse(
            '<div class="text-red-500">Ungültiger Context</div>', status=400
        )

    # 2. Engine initialisieren
    engine = IconChallengeEngine(request, context_type)

    # 3. Challenge generieren
    challenge_data = engine.generate_challenge()

    # 4. Config für Template
    config = CHALLENGE_CONTEXTS[context_type]

    # 5. Template-Context zusammenbauen
    context = {
        "icons": challenge_data["icons"],  # [(name, svg), ...]
        "target_icon": challenge_data["target_icon"],  # 'heart'
        "target_svg": challenge_data["target_svg"],  # '<svg>...</svg>'
        "context_type": context_type,  # 'guest'
        "title": config["title"],  # '🔐 Gast-Zugang'
        "description": config["description"],  # 'Terminal Check'
        "min_count": config["min_count"],  # 1
        "max_count": config["max_count"] + 1,  # 5 (für Buttons 1-5)
    }

    # 6. Render Modal
    return render(request, "icon_challenge/modal.html", context)


# ============================================
# 2. CHALLENGE VERIFIZIEREN (Antwort prüfen)
# ============================================


@require_POST
def verify_challenge_attempt(request, context_type):
    """
    Prüfe User-Antwort

    POST-Data:
        count: int (User-Antwort, z.B. 3)

    Returns:
        HTML: Success/Error Message
    """
    # 1. Validierung
    if context_type not in CHALLENGE_CONTEXTS:
        return HttpResponse(
            '<div class="text-red-500">Ungültiger Context</div>', status=400
        )

    # 2. User-Antwort holen
    user_count = request.POST.get("count")

    if not user_count:
        return HttpResponse(
            '<div class="text-red-500 font-bold">❌ Keine Antwort!</div>'
        )

    # 3. Engine initialisieren
    engine = IconChallengeEngine(request, context_type)

    # 4. Verifizieren
    result = engine.verify_attempt(user_count)

    # 5. Rate Limit aktiv?
    if result.get("blocked"):
        return render_error_message(
            result["message"],
            wait_time=result.get("wait_time", 0),
            level=result.get("level", "warning"),
        )

    # 6. Richtig oder Falsch?
    if result["success"]:
        # ✅ RICHTIG! → Führe Context-Action aus
        return handle_success(request, context_type)
    else:
        # ❌ FALSCH! → Zeige Fehler + neue Challenge laden
        return render_error_message(
            result["message"], reload_challenge=True, context_type=context_type
        )


# ============================================
# SIGNUP INTEGRATION
# ============================================


@require_POST
def signup_prepare(request):
    """
    Schritt 1 (Signup): Validiere + speichere Daten
    Schritt 2: Öffne Icon-Challenge Modal
    """
    # 1. Form-Daten holen
    email = request.POST.get("email", "").strip()
    password1 = request.POST.get("password1", "")
    password2 = request.POST.get("password2", "")

    # 2. Basic Validation
    if not email or not password1 or not password2:
        return HttpResponse(
            """
            <div class='bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 
                        p-4 rounded-xl border-2 border-red-500 font-bold text-center'>
                ❌ Bitte alle Felder ausfüllen!
            </div>
        """
        )

    if password1 != password2:
        return HttpResponse(
            """
            <div class='bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 
                        p-4 rounded-xl border-2 border-red-500 font-bold text-center'>
                ❌ Passwörter stimmen nicht überein!
            </div>
        """
        )

    if len(password1) < 8:
        return HttpResponse(
            """
            <div class='bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 
                        p-4 rounded-xl border-2 border-red-500 font-bold text-center'>
                ❌ Passwort muss mindestens 8 Zeichen lang sein!
            </div>
        """
        )

    # 3. Prüfe ob Email schon existiert
    from django.contrib.auth import get_user_model

    User = get_user_model()

    if User.objects.filter(email=email).exists():
        return HttpResponse(
            """
            <div class='bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 
                        p-4 rounded-xl border-2 border-red-500 font-bold text-center'>
                ❌ Diese Email ist bereits registriert!
                <a href="{% url 'account_login' %}" class="underline ml-2">Zum Login</a>
            </div>
        """
        )

    # 4. Speichere in Session
    request.session["signup_data"] = {
        "email": email,
        "password1": password1,
        "password2": password2,
    }

    # 5. Triggere Icon-Challenge Modal
    return HttpResponse(
        """
        <div hx-get="/icon-challenge/start/signup/"
             hx-trigger="load"
             hx-target="#modal-container"
             hx-swap="innerHTML">
        </div>
        <div class='bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 
                    p-4 rounded-xl border-2 border-blue-500 font-bold text-center'>
            🔐 Bitte löse die Sicherheits-Challenge...
        </div>
    """
    )


# ============================================
# CONTACT INTEGRATION
# ============================================


@require_POST
def contact_prepare(request):
    """
    Schritt 1 (Contact): Validiere + speichere Daten
    Schritt 2: Öffne Icon-Challenge Modal
    """
    # 1. Honeypot Check
    if request.POST.get("website"):
        # Bot detected! Fake success
        return HttpResponse(
            """
            <div class='bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 
                        p-4 rounded-xl border-2 border-green-500 font-bold text-center'>
                ✅ Nachricht erfolgreich versendet!
            </div>
        """
        )

    # 2. Form-Daten holen
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    company = request.POST.get("company", "").strip()
    subject = request.POST.get("subject", "").strip()
    message = request.POST.get("message", "").strip()

    # 3. Basic Validation
    if not all([name, email, subject, message]):
        return HttpResponse(
            """
            <div class='bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 
                        p-4 rounded-xl border-2 border-red-500 font-bold text-center'>
                ❌ Bitte fülle alle Pflichtfelder aus!
            </div>
        """
        )

    # 4. Speichere in Session
    request.session["contact_data"] = {
        "name": name,
        "email": email,
        "company": company,
        "subject": subject,
        "message": message,
    }

    # 5. Triggere Icon-Challenge Modal
    return HttpResponse(
        """
        <div hx-get="/icon-challenge/start/contact/"
             hx-trigger="load"
             hx-target="#modal-container"
             hx-swap="innerHTML">
        </div>
        <div class='bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-400 
                    p-4 rounded-xl border-2 border-blue-500 font-bold text-center'>
            🔐 Bitte löse die Sicherheits-Challenge...
        </div>
    """
    )


# ============================================
# 3. SUCCESS HANDLER (Context-spezifische Actions)
# ============================================


def handle_success(request, context_type):
    """
    Challenge bestanden! Führe Action aus.

    guest → Login Guest-User
    contact → Sende Email
    signup → Erstelle Account
    """

    if context_type == "guest":
        # GUEST: Login Guest-User
        User = get_user_model()
        try:
            guest_user = User.objects.get(username="guest")
            login(
                request, guest_user, backend="django.contrib.auth.backends.ModelBackend"
            )

            # Session-Daten setzen
            request.session["is_guest"] = True
            request.session["guest_login_time"] = time.time()

            # Cleanup Challenge-Session
            cleanup_challenge(request, "guest")

            # HTMX Redirect zu /projects/
            response = HttpResponse(
                """
                <div class="text-cyan-400 font-black uppercase text-xl animate-pulse text-center">
                    ✅ Zugang gewährt...
                </div>
            """
            )
            response["HX-Redirect"] = "/projects/secret-lab/"
            return response

        except User.DoesNotExist:
            return HttpResponse(
                """
                <div class="text-red-500 font-bold text-center">
                    ❌ Fehler: Guest-User nicht gefunden!
                </div>
            """
            )

    elif context_type == "contact":
        # CONTACT: Sende Email direkt

        # 1. Hole Daten aus Session
        contact_data = request.session.get("contact_data", {})

        if not contact_data:
            return HttpResponse(
                """
                <div class='text-red-500 font-bold text-center'>
                    ❌ Session abgelaufen. Bitte nochmal probieren.
                </div>
            """
            )

        # 2. Email-Texte bauen
        email_body_to_you = f"""
🔔 Neue Kontaktanfrage über dein Portfolio!

Von: {contact_data['name']}
Email: {contact_data['email']}
Unternehmen: {contact_data.get('company') or 'Nicht angegeben'}
Betreff: {contact_data['subject']}

Nachricht:
{contact_data['message']}

---
💡 TIPP: Einfach auf diese Email ANTWORTEN um {contact_data['name']} direkt zu kontaktieren!
Die Antwort geht automatisch an: {contact_data['email']}
        """

        confirmation_body = f"""
Hallo {contact_data['name']},

vielen Dank für deine Nachricht! 🎉

Ich habe deine Anfrage erhalten und melde mich so schnell wie möglich bei dir – in der Regel innerhalb von 24 Stunden.

Hier nochmal deine Nachricht zur Sicherheit:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Betreff: {contact_data['subject']}

{contact_data['message']}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Falls du noch etwas ergänzen möchtest, antworte einfach auf diese Email!

Beste Grüße,
Martin Freimuth
Fullstack Developer
        """

        # 3. Sende Emails via Resend API
        resend_url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {settings.RESEND_API_KEY}",
            "Content-Type": "application/json",
        }

        try:
            # Email an DICH
            payload_to_me = {
                "from": "Portfolio Contact <noreply@martin-freimuth.dev>",
                "to": "mat.frei@gmx.de",
                "subject": f"📬 Kontaktanfrage: {contact_data['subject']}",
                "reply_to": contact_data["email"],  # User kann dir antworten!
                "text": email_body_to_you,
            }
            resp_me = requests.post(
                resend_url, headers=headers, json=payload_to_me, timeout=10
            )

            if resp_me.ok:
                # Bestätigung an USER
                payload_to_user = {
                    "from": "Martin Freimuth <hi@martin-freimuth.dev>",  # ← PERSÖNLICH!
                    "to": contact_data["email"],
                    "subject": "✅ Deine Nachricht wurde empfangen",
                    "reply_to": "hi@martin-freimuth.dev",  # ← User kann dir antworten!
                    "text": confirmation_body,
                }
                requests.post(
                    resend_url, headers=headers, json=payload_to_user, timeout=10
                )

                # Cleanup
                cleanup_challenge(request, "contact")
                request.session.pop("contact_data", None)

                return HttpResponse(
                    f"""
    <script>
        // Modal schließen
        document.getElementById('modal-container').innerHTML = '';
        
        // Formular sofort leeren
        setTimeout(() => {{
            const form = document.getElementById('contact-form');
            if (form) form.reset();
        }}, 2000);
        
        // Success-Message nach 5s ausblenden
        setTimeout(() => {{
            const resultDiv = document.getElementById('contact-result');
            if (resultDiv) {{
                resultDiv.style.transition = 'opacity 0.5s';
                resultDiv.style.opacity = '0';
                setTimeout(() => {{
                    resultDiv.innerHTML = '';
                    resultDiv.style.opacity = '1';
                }}, 500);
            }}
        }}, 5000);
    </script>
    
    <div class='bg-green-100 dark:bg-green-900/30 
                text-green-700 dark:text-green-400 
                p-8 rounded-3xl border-2 border-green-500 
                font-bold text-center shadow-xl'>
        
        <div class="text-6xl mb-4 animate-bounce">✅</div>
        
        <div class="text-2xl mb-3">
            Nachricht erfolgreich versendet!
        </div>
        
        <div class="text-lg mb-4">
            Du erhältst gleich eine Bestätigungs-Email an:<br>
            <span class="font-black">{contact_data['email']}</span>
        </div>
        
        <div class="text-sm text-gray-600 dark:text-gray-400">
            Ich melde mich in Kürze bei dir.
        </div>
    </div>
"""
                )
            else:
                return HttpResponse(
                    """
                    <div class='text-red-500 font-bold text-center'>
                        ❌ Email-Versand fehlgeschlagen. Bitte versuche es später nochmal.
                    </div>
                """
                )

        except Exception as e:
            return HttpResponse(
                f"""
                <div class='text-red-500 font-bold text-center'>
                    ❌ Verbindungsfehler: {str(e)}
                </div>
            """
            )

    elif context_type == "signup":
        # SIGNUP: Erstelle Account

        # 1. Hole Daten aus Session
        signup_data = request.session.get("signup_data", {})

        if not signup_data:
            return HttpResponse(
                """
                <div class='text-red-500 font-bold text-center'>
                    ❌ Session abgelaufen. Bitte nochmal probieren.
                </div>
            """
            )

        # 2. Erstelle User
        User = get_user_model()

        try:
            user = User.objects.create_user(
                username=signup_data["email"],
                email=signup_data["email"],
                password=signup_data["password1"],
            )

            # 3. Email-Address für Allauth erstellen
            email_address = EmailAddress.objects.create(
                user=user, email=signup_data["email"], primary=True, verified=False
            )

            # 4. Sende Verification-Email
            email_address.send_confirmation(request)

            # 5. Cleanup Session
            cleanup_challenge(request, "signup")
            request.session.pop("signup_data", None)

            # 6. Success Message + Redirect
            return HttpResponse(
                """
                <script>
                    document.getElementById('modal-container').innerHTML = '';
                    setTimeout(function() {
                        window.location.href = '/accounts/login/';
                    }, 3000);
                </script>
                <div class='bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 
                            p-6 rounded-2xl border-2 border-green-500 font-bold text-center'>
                    ✅ Account erfolgreich erstellt!
                    <div class='mt-4 text-sm'>
                        📧 Bitte prüfe deine Emails zur Bestätigung.
                        <br/>
                        <span class='text-xs opacity-75'>Weiterleitung in 3 Sekunden...</span>
                    </div>
                </div>
            """
            )

        except Exception as e:
            return HttpResponse(
                f"""
                <div class='text-red-500 font-bold text-center'>
                    ❌ Fehler beim Erstellen des Accounts: {str(e)}
                </div>
            """
            )

    else:
        return HttpResponse(
            """
            <div class="text-red-500">Unbekannter Context</div>
        """
        )


# ============================================
# 4. HELPER FUNCTIONS
# ============================================


def render_error_message(
    message, wait_time=0, level="warning", reload_challenge=False, context_type=None
):
    """
    Rendere Fehler-Message mit optionalem Countdown

    Args:
        message: Fehlertext
        wait_time: Sekunden warten (für Rate Limit)
        level: 'warning' oder 'danger'
        reload_challenge: Neue Challenge laden?
        context_type: 'guest', 'contact', 'signup'
    """

    # Farben basierend auf Level
    colors = {
        "warning": {
            "bg": "bg-yellow-100 dark:bg-yellow-900/30",
            "text": "text-yellow-700 dark:text-yellow-400",
            "border": "border-yellow-500",
        },
        "danger": {
            "bg": "bg-red-100 dark:bg-red-900/30",
            "text": "text-red-700 dark:text-red-400",
            "border": "border-red-500",
        },
    }

    color = colors.get(level, colors["warning"])

    # HTML bauen
    html = f"""
    <div class="{color['bg']} {color['text']} {color['border']} 
                border-2 rounded-2xl p-6 font-bold text-center 
                animate-shake">
        {message}
    """

    # Countdown-Timer (falls Rate Limit aktiv)
    if wait_time > 0:
        html += f"""
        <div class="mt-4 text-sm uppercase tracking-wider">
            Warte noch: <span id="countdown-timer" class="font-black">{wait_time}</span>s
        </div>
        <script>
            (function() {{
                let remaining = {wait_time};
                const display = document.getElementById('countdown-timer');
                
                const interval = setInterval(() => {{
                    remaining--;
                    if (display) display.innerText = remaining;
                    
                    if (remaining <= 0) {{
                        clearInterval(interval);
                        // Timer abgelaufen → Message entfernen
                        display.closest('div').innerHTML = 
                            '<span class="text-gray-400 text-sm uppercase">Bereit für neuen Versuch...</span>';
                    }}
                }}, 1000);
            }})();
        </script>
        """

    html += "</div>"

    # Neue Challenge laden (falls Antwort falsch war)
    if reload_challenge and context_type:
        html += f"""
        <div 
            hx-get="/icon-challenge/start/{context_type}/"
            hx-trigger="load delay:1s"
            hx-target="#modal-container"
            hx-swap="innerHTML"
        ></div>
        """

    return HttpResponse(html)
