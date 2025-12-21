from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import time
import random

# 1. Die ICON_MAP (Sorgt dafür, dass die Icons im Modal erscheinen)
ICON_MAP = {
    "anchor": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><path d="M12 22v-4M5 12H2a10 10 0 0 0 20 0h-3M12 5V2M12 5c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>',
    "ship": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><path d="M2 21c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1 .6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M19.38 20A11.6 11.6 0 0 0 21 14l-9-4-9 4c0 2.2.94 4.19 2.43 5.58"/></svg>',
    "wind": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"/></svg>',
    "waves": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><path d="M2 6c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1 .6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1 .6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1 .6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/></svg>',
    "sun": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>',
    "moon": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>',
    "cloud": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><path d="M17.5 19c2.5 0 4.5-2 4.5-4.5 0-2.3-1.7-4.2-3.9-4.5-1-3-3.8-5-6.6-5a7 7 0 0 0-6.8 5.7c-2.1.4-3.7 2.2-3.7 4.3 0 2.5 2 4.5 4.5 4.5h12z"/></svg>',
    "compass": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/></svg>',
    "cpu": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><rect x="4" y="4" width="16" height="16" rx="2"/><path d="M9 2v2M15 2v2M9 20v2M15 20v2M20 9h2M20 15h2M2 9h2M2 15h2"/></svg>',
    "database": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>',
    "terminal": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>',
    "code": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><polyline points="16 18 22 12 16 6"/><polyline points="8 6 2 12 8 18"/></svg>',
    "mouse": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><rect x="5" y="2" width="14" height="20" rx="7"/><path d="M12 6v4"/></svg>',
    "keyboard": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="M6 8h.01M10 8h.01M14 8h.01M18 8h.01M6 12h.01M10 12h.01M14 12h.01M18 12h.01M7 16h10"/></svg>',
    "hard-drive": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><line x1="22" y1="12" x2="2" y2="12"/><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>',
    "monitor": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>',
    "star": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>',
    "bell": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg>',
    "camera": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>',
    "map-pin": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>',
    "settings": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>',
    "key": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><path d="M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.778-7.778zM12 12l.4 1h1.1l.4 1h1.1l.4 1h1.1L19 18"/></svg>',
    "coffee": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><path d="M18 8h1a4 4 0 0 1 0 8h-1M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8zM6 1v3M10 1v3M14 1v3"/></svg>',
    "beer": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><path d="M17 11h1a3 3 0 0 1 0 6h-1M5 21h12V7H5v14zM5 3h12"/></svg>',
    "gift": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><polyline points="20 12 20 22 4 22 4 12"/><rect x="2" y="7" width="20" height="5"/><line x1="12" y1="22" x2="12" y2="7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/></svg>',
    "flag": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/></svg>',
    "trash": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>',
    "home": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "message": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "search": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>',
    "check": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><polyline points="20 6 9 17 4 12"/></svg>',
    "x": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
    "up": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><polyline points="18 15 12 9 6 15"/></svg>',
    "down": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><polyline points="6 9 12 15 18 9"/></svg>',
    "left": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><polyline points="15 18 9 12 15 6"/></svg>',
    "right": '<svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" stroke-width="2" fill="none"><polyline points="9 18 15 12 9 6"/></svg>',
}


# 2. View für das Gast-Modal (Challenge erstellen)
def get_guest_modal(request):
    icon_names = list(ICON_MAP.keys())
    target_name = random.choice(icon_names)
    request.session["target_icon"] = target_name

    sample_size = min(len(icon_names), 40)
    display_names = random.sample(icon_names, sample_size)
    if target_name not in display_names:
        display_names[0] = target_name
    random.shuffle(display_names)

    icons_to_render = [(name, ICON_MAP[name]) for name in display_names]

    return render(
        request,
        "accounts/partials/guest_modal.html",
        {"icons": icons_to_render, "target_name": target_name},
    )


# 3. View für den Login-Versuch
def guest_login_attempt(request):
    attempts = request.session.get("guest_attempts", 0)
    last_attempt = request.session.get("last_guest_attempt", 0)
    current_time = time.time()

    # --- 3.1 Cooldown Logik mit stillem Reset auf 1 ---
    cooldown = 0
    if attempts >= 5:
        cooldown = 60
    elif attempts >= 3:
        cooldown = 30

    time_passed = current_time - last_attempt

    if time_passed < cooldown:
        # Sperre ist noch aktiv -> Timer anzeigen
        wait_time = int(cooldown - time_passed)
        level = "MAXIMAL-SPERRE" if attempts >= 5 else "SICHERHEITS-SPERRE"
        return HttpResponse(
            f'<div class="animate-shake flex flex-col items-center">'
            f'  <span class="text-red-500 font-black text-xl tracking-tighter uppercase">{level}</span>'
            f'  <span class="text-red-400/70 text-xs tracking-widest uppercase mt-2">'
            f'    System-Reset in <span id="countdown-sec" class="text-red-500 font-bold">{wait_time}</span>s'
            f"  </span>"
            f"  <script>"
            f"    (function() {{"
            f"      let sec = {wait_time};"
            f'      const el = document.getElementById("countdown-sec");'
            f"      const timer = setInterval(() => {{"
            f"        sec--;"
            f"        if (el) el.innerText = (sec > 0) ? sec : 0;"
            f"        if (sec <= 0) clearInterval(timer);"
            f"      }}, 1000);"
            f"    }})();"
            f"  </script>"
            f"</div>"
        )
    elif attempts >= 3:
        # SPERRE ABGELAUFEN: Stillschweigender Reset auf 1 Versuch
        # Der User merkt es erst, wenn er wieder klickt.
        request.session["guest_attempts"] = 1
        attempts = 1
        # Der Code läuft jetzt einfach weiter zur Icon-Prüfung

    selected = request.POST.get("selected_icon")
    correct = request.session.get("target_icon")

    # 3.2 Logik für RICHTIGES Icon (Bleibt gleich)
    if selected == correct:
        try:
            guest_user = User.objects.get(username="guest")
            login(
                request, guest_user, backend="django.contrib.auth.backends.ModelBackend"
            )

            # --- NEU: Startzeit für die Sitzung speichern ---
            request.session["guest_login_time"] = time.time()

            request.session["is_guest"] = True
            request.session["guest_attempts"] = 0

            response = HttpResponse(
                '<span class="text-cyan-400 font-black uppercase text-xl animate-pulse">Zugang gewährt...</span>'
            )
            response["HX-Redirect"] = "/"
            return response
        except Exception as e:
            return HttpResponse(
                f'<span class="text-red-600 font-bold">Fehler: {str(e)}</span>'
            )

    # --- 3.3 Logik für FALSCHES Icon ---
    else:
        attempts += 1
        request.session["guest_attempts"] = attempts
        request.session["last_guest_attempt"] = current_time

        if attempts == 3:
            # Erste Sperre auslösen
            return HttpResponse(
                f'<div class="flex flex-col items-center">'
                f'  <span class="text-red-500 font-bold uppercase text-lg">3. Fehlversuch: 30s Sperre!</span>'
                f'  <span class="text-red-400/70 text-xs mt-2 uppercase">Warten Sie <span id="init-timer">30</span>s...</span>'
                f"  <script>"
                f"    (function() {{"
                f'       let s=30; const e=document.getElementById("init-timer");'
                f"       const t = setInterval(() => {{ if(s>0) s--; if(e) e.innerText=s; if(s<=0) clearInterval(t); }}, 1000);"
                f"    }})();"
                f"  </script>"
                f"</div>"
            )
        elif attempts == 4:
            return HttpResponse(
                '<span class="text-pink-500 font-bold uppercase tracking-widest text-lg">Letzte Warnung! (Noch 1 Versuch)</span>'
            )
        elif attempts >= 5:
            # Maximale Sperre auslösen
            return HttpResponse(
                f'<div class="flex flex-col items-center">'
                f'  <span class="text-red-600 font-black uppercase text-lg">LIMIT ERREICHT: 60s Sperre!</span>'
                f'  <span class="text-red-500/70 text-xs mt-2 uppercase">Sperre aktiv: <span id="max-timer">60</span>s...</span>'
                f"  <script>"
                f"    (function() {{"
                f'       let s=60; const e=document.getElementById("max-timer");'
                f"       const t = setInterval(() => {{ if(s>0) s--; if(e) e.innerText=s; if(s<=0) clearInterval(t); }}, 1000);"
                f"    }})();"
                f"  </script>"
                f"</div>"
            )
        else:
            needed = 3 - attempts
            return HttpResponse(
                f'<span class="text-pink-500 font-bold uppercase tracking-widest text-lg">Zugang  verweigert! ({needed} Versuche)</span>'
            )


# 4. Standard Registrierungs-View
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("core:home")
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


# 5. Log Out Funktion für "guest"
def guest_timer(request):
    # Nur für eingeloggte Gäste
    if request.user.is_authenticated and request.session.get("is_guest"):
        login_time = request.session.get("guest_login_time", 0)
        limit = 120  # 5 Minuten (120Sekunden) - hier kannst du die Zeit anpassen
        elapsed = time.time() - login_time
        remaining = int(limit - elapsed)

        if remaining <= 0:
            logout(request)
            return {"guest_remaining": 0}

        return {"guest_remaining": remaining}
    return {}


# 6. guest ausloggen
@login_required
def secret_lab(request):
    # --- GAST-TIMER PRÜFUNG ---
    if request.user.is_authenticated and request.session.get("is_guest"):
        login_time = request.session.get("guest_login_time", 0)
        limit = 120 

        elapsed = time.time() - login_time

        if elapsed > limit:
            # Sitzung abgelaufen!
            logout(request)
            messages.warning(
                request, "Sitzung abgelaufen: Sicherheits-Reset durchgeführt."
            )
            return redirect("account_login")
    # --- ENDE PRÜFUNG ---

    # Hier kommt dein normaler Code für das Secret Lab
    return render(request, "projects/secret_lab.html")
