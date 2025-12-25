from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import time











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
