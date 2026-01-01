import requests
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from projects.models import Project
from .models import Profile, PortfolioScreenshot
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from .models import ProjectUpdate, ColoredTag


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

def in_progress(request):
    """
    Generic 'In Progress' page für Features die entwickelt werden
    """
    return render(request, 'core/in_progress.html')


@login_required(login_url='/accounts/login/')
def about_portfolio(request):
    """
    Technische Dokumentation mit Screenshots.
    Nur für eingeloggte User (Guest oder Registered).
    """
    # Screenshots nach Sektion gruppieren
    screenshots = {
        'overview': PortfolioScreenshot.objects.filter(section='overview'),
        'architecture': PortfolioScreenshot.objects.filter(section='architecture'),
        'auth': PortfolioScreenshot.objects.filter(section='auth'),
        'deployment': PortfolioScreenshot.objects.filter(section='deployment'),
        'challenges': PortfolioScreenshot.objects.filter(section='challenges'),
        'apis': PortfolioScreenshot.objects.filter(section='apis'),
    }
    
    return render(request, 'core/about_portfolio.html', {
        'screenshots': screenshots
    })


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

        # Die schönen Texte 
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

            # --- ÄNDERUNG HIER: Wir prüfen auf .ok (Status 200-299) ---
            if resp_me.ok:
                # 2. Bestätigung an USER
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

                messages.success(request, "✅ Nachricht erfolgreich versendet! Ich melde mich in Kürze.")
            else:
                # Nur wenn es wirklich schiefgeht (z.B. Status 403, 500)
                print(f"Resend API Error: {resp_me.text}")
                messages.error(request, "❌ Ups, da gab es ein Problem mit dem Mail-Dienst. Bitte versuche es später nochmal.")

        except Exception as e:
            print(f"API Connection Error: {e}")
            messages.error(request, "❌ Verbindung fehlgeschlagen. Bitte prüfe dein Netzwerk.")

    return render(request, "core/contact.html")


# ==========================================
# CURRENT PROJECT VIEWS
# ==========================================




def current_project(request):
    """Current Project - Full Page"""
    selected_tags = request.GET.getlist('tags')
    updates = get_filtered_updates(selected_tags)
    all_tags = ColoredTag.objects.all().order_by('name')
    
    context = {
        'updates': updates,
        'all_tags': all_tags,
        'selected_tags': selected_tags,
    }
    
    return render(request, 'core/current_project.html', context)


def update_list_htmx(request):
    """HTMX Partial: Filter Pills + Updates"""
    selected_tags = request.GET.getlist('tags')
    updates = get_filtered_updates(selected_tags)
    all_tags = ColoredTag.objects.all().order_by('name')
    
    # Tag query für Modal
    tag_query = '&'.join([f'tags={tag}' for tag in selected_tags])
    
    return render(request, 'core/partials/filter_and_updates.html', {
        'updates': updates,
        'all_tags': all_tags,     # ← WICHTIG für Pills!
        'selected_tags': selected_tags,
        'tag_query': tag_query,
    })


def update_detail_htmx(request, pk):
    """HTMX Partial: Modal Content"""
    update = get_object_or_404(ProjectUpdate, pk=pk)
    selected_tags = request.GET.getlist('tags')
    
    # Next/Previous (berücksichtigt Filter!)
    filtered_updates = get_filtered_updates(selected_tags)
    update_ids = list(filtered_updates.values_list('id', flat=True))
    
    try:
        current_index = update_ids.index(update.id)
        next_id = update_ids[current_index + 1] if current_index + 1 < len(update_ids) else None
        prev_id = update_ids[current_index - 1] if current_index > 0 else None
    except (ValueError, IndexError):
        next_id = prev_id = None
    
    # Query-String für Filter
    tag_query = '&'.join([f'tags={tag}' for tag in selected_tags])
    
    return render(request, 'core/partials/update_modal.html', {
        'update': update,
        'next_id': next_id,
        'prev_id': prev_id,
        'selected_tags': selected_tags,
        'tag_query': tag_query,
    })


def get_filtered_updates(selected_tags):
    """Helper: Filtered & Sorted Updates"""
    updates = ProjectUpdate.objects.filter(is_current=True)
    
    if selected_tags:
        # Smart Sorting: Meiste Tag-Matches zuerst!
        updates = updates.filter(
            tags__slug__in=selected_tags
        ).annotate(
            tag_match_count=Count('tags', filter=Q(tags__slug__in=selected_tags))
        ).filter(
            tag_match_count__gt=0
        ).order_by('-tag_match_count', '-created_at').distinct()
    else:
        updates = updates.order_by('-created_at')
    
    return updates


