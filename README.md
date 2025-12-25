# 🚀 Django Portfolio - Production-Ready Web Application

<div align="center">

![Django](https://img.shields.io/badge/Django-5.1-green?style=for-the-badge&logo=django)
![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Latest-blue?style=for-the-badge&logo=postgresql)
![HTMX](https://img.shields.io/badge/HTMX-2.0-purple?style=for-the-badge)
![Tailwind](https://img.shields.io/badge/Tailwind-3.x-cyan?style=for-the-badge&logo=tailwindcss)
![Railway](https://img.shields.io/badge/Deployed_on-Railway-black?style=for-the-badge)

**Live Demo:** [https://martin-freimuth.dev](https://martin-freimuth.dev)

*A full-stack Django portfolio showcasing modern web development practices, custom authentication, privacy-first bot protection, and production deployment.*

</div>

---

## 📑 **Table of Contents**

1. [🎯 Project Overview](#-project-overview)
2. [✨ Key Features](#-key-features)
3. [🏗️ Architecture](#️-architecture)
4. [🔐 Icon-Challenge System](#-icon-challenge-system-privacy-first-captcha)
5. [🚀 Quick Start](#-quick-start)
6. [💻 Local Development Setup](#-local-development-setup)
7. [📦 Tech Stack](#-tech-stack)
8. [🌐 Deployment](#-deployment)
9. [🔧 Configuration](#-configuration)
10. [📖 API Documentation](#-api-documentation)
11. [🧪 Testing](#-testing)
12. [🤝 Contributing](#-contributing)
13. [📄 License](#-license)

---

## 🎯 **Project Overview**

This portfolio is **more than just a website** – it's a complete Django application demonstrating production-ready web development:

### **What Makes This Special?**

- **🔐 Custom CAPTCHA Alternative**: Privacy-first icon-challenge system (no Google reCAPTCHA tracking)
- **⏱️ Context Processor Pattern**: Live guest-session timer without JavaScript frameworks
- **🤖 Lightweight AI Integration**: Direct REST API calls to Google Gemini (no heavy SDK)
- **☁️ Hybrid Storage**: Cloudinary for media, Whitenoise for static files
- **🛡️ Multi-Layer Bot Protection**: Honeypot + Icon-Challenge + Rate Limiting + Email Verification
- **📱 Fully Responsive**: Mobile-first design with dark mode support

### **Use Cases**

This project demonstrates:
- Multi-tier authentication (Guest/User/Admin)
- Privacy-compliant bot protection
- Production deployment on Railway
- HTMX-powered dynamic UI without page reloads
- Session-based state management
- External API integrations (Resend, Gemini, Cloudinary)

---

## ✨ **Key Features**

### **1. Multi-Tier Authentication**

| Tier | Access Level | Duration | Use Case |
|------|--------------|----------|----------|
| **Guest** | Limited (Public + Demo Projects) | 2 minutes | Quick portfolio preview for recruiters |
| **User** | Full access | 24 hours | Registered users with email verification |
| **Admin** | Admin panel | Unlimited | Project management & content updates |

### **2. Icon-Challenge Bot Protection**

**Privacy-First CAPTCHA Alternative** - Zero tracking, GDPR-compliant:

- **3×3 Icon Grid**: 9 random icons from 40-icon pool (Lucide Icons)
- **Count Challenge**: "How many ❤️ do you see?" (2-4 occurrences)
- **Progressive Rate Limiting**: 3 attempts → 30s cooldown, 5 attempts → 60s
- **Context-Aware**: Different settings for Guest/Contact/Signup
- **New Icons on Error**: Prevents pattern recognition by bots

### **3. Dual-Mode Portfolio**

- **Public Mode**: Showcases selected demo projects
- **Secret Lab**: Full project access after authentication
- **Intelligent Switching**: Automatic based on auth status

### **4. Production-Ready Deployment**

- ✅ **Railway PaaS**: Auto-scaling, zero-downtime deploys
- ✅ **PostgreSQL**: Production database
- ✅ **Custom Domain**: HTTPS with auto-renewed Let's Encrypt certs
- ✅ **Cloudinary CDN**: Global image delivery
- ✅ **Whitenoise**: Compressed static file serving

---

## 🏗️ **Architecture**

### **Django Apps Structure**
```
portfolio_site/
├── accounts/              # Custom Authentication & Guest System
│   ├── management/
│   │   └── commands/
│   │       ├── create_guest_user.py    # Setup guest account
│   │       └── cleanup_loginlogs.py    # GDPR compliance (90-day cleanup)
│   ├── models.py          # LoginLog (IP tracking, User-Agent)
│   ├── views.py           # Guest timer context processor
│   └── signals.py         # Auto-logging on login/logout
│
├── icon_challenge/        # 🆕 Privacy-First Bot Protection
│   ├── config.py          # 40 Icons pool + context settings
│   ├── engine.py          # Core challenge logic (DRY)
│   │   ├── generate_challenge()      # 3×3 grid generation
│   │   ├── verify_attempt()          # Count verification
│   │   └── handle_rate_limiting()    # Progressive cooldowns
│   ├── views.py           # HTMX endpoints
│   │   ├── start_challenge()         # Modal rendering
│   │   ├── verify_challenge_attempt() # Answer validation
│   │   ├── handle_success()          # Context-specific actions
│   │   ├── contact_prepare()         # Contact form integration
│   │   └── signup_prepare()          # Signup integration
│   ├── urls.py            # URL routing
│   └── templates/
│       └── modal.html     # Reusable 3×3 grid template
│
├── core/                  # Landing Pages & Static Content
│   ├── models.py          # Profile (Cloudinary images)
│   ├── views.py           # Contact form (Resend API)
│   └── templates/
│       ├── home.html
│       ├── about.html
│       ├── contact.html
│       └── about_portfolio.html   # Technical documentation
│
├── projects/              # Portfolio Management
│   ├── models.py          # Project, InvitedUser
│   ├── views.py           # Dual-mode logic (public/secret)
│   └── templates/
│       ├── public_list.html
│       └── secret_lab.html
│
├── bmi_app/               # BMI Calculator + AI Health Tips
│   └── views.py           # ask_gemini_rest() - Direct API call
│
├── rps_app/               # Rock Paper Scissors Game
│   └── views.py           # Session-based game state
│
└── legal/                 # GDPR Compliance
    ├── views.py           # Impressum + Datenschutz
    └── templates/
        ├── impressum.html
        └── datenschutz.html
```

### **Data Flow Diagram**
```
┌─────────────┐
│   Browser   │
│  (HTTPS)    │
└──────┬──────┘
       │
       ↓
┌─────────────────────────────────────────┐
│  Railway (Gunicorn + Django)            │
│  ├─ Whitenoise Middleware (Static)      │
│  ├─ Django Apps (Business Logic)        │
│  └─ Context Processors (Guest Timer)    │
└──────┬──────────────────────────────────┘
       │
       ├──→ PostgreSQL (User data, Projects, Login logs)
       │
       ├──→ Cloudinary (Uploaded images, Thumbnails)
       │
       ├──→ Resend API (Transactional emails)
       │
       └──→ Google Gemini API (AI health tips)
```

### **Request Lifecycle Example**
```python
# User requests: GET /projects/

1. Django Middleware Stack
   ├─ SecurityMiddleware (HTTPS redirect, headers)
   ├─ WhitenoiseMiddleware (static file serving)
   ├─ SessionMiddleware (load session)
   ├─ AuthenticationMiddleware (load user)
   └─ CSRF Middleware (token validation)

2. URL Routing
   /projects/ → projects.views.public_list()

3. View Logic
   ├─ Check request.user.is_authenticated
   ├─ Query: Project.objects.filter(is_public_demo=True) or .all()
   └─ Render template

4. Context Processor (guest_timer)
   ├─ Calculate remaining time if guest
   └─ Add to template context

5. Template Rendering
   ├─ base.html (nav, timer, footer)
   └─ project cards (dynamic based on auth)

6. Response
   HTTP 200 OK + HTML
```

---

## 🔐 **Icon-Challenge System (Privacy-First CAPTCHA)**

### **The Problem**

Traditional solutions have issues:
- ❌ **Google reCAPTCHA**: Tracks users, GDPR concerns
- ❌ **No CAPTCHA**: Vulnerable to bot attacks
- ❌ **Complex alternatives**: Poor UX, expensive

### **Our Solution: Icon-Challenge**

**A custom, privacy-first bot protection system using icon recognition.**

### **How It Works**
```
┌──────────────────────────────────────────┐
│  1. User triggers action (Login/Contact) │
└─────────────┬────────────────────────────┘
              │
              ↓
┌──────────────────────────────────────────┐
│  2. Engine generates 3×3 grid:            │
│     - 40 icons pool (Lucide Icons)       │
│     - Target icon appears 2-4 times      │
│     - Other icons fill remaining slots   │
│     - Random shuffle                     │
└─────────────┬────────────────────────────┘
              │
              ↓
┌──────────────────────────────────────────┐
│  3. User counts target icons             │
│     - "How many ❤️ do you see?"          │
│     - Clicks count (1-5)                 │
└─────────────┬────────────────────────────┘
              │
              ↓
┌──────────────────────────────────────────┐
│  4. Engine verifies answer                │
│     ✓ Correct → Execute action           │
│     ✗ Wrong → New challenge + rate limit │
└──────────────────────────────────────────┘
```

### **Architecture: One Engine, Three Use Cases**
```python
# icon_challenge/config.py
CHALLENGE_CONTEXTS = {
    'guest': {
        'title': '🔐 Gast-Zugang',
        'cooldown_3': 30,  # 30s after 3 attempts
        'cooldown_5': 60,  # 60s after 5 attempts
    },
    'contact': {
        'title': '📧 Kontakt-Verifizierung',
        'cooldown_3': 30,
        'cooldown_5': 60,
    },
    'signup': {
        'title': '✨ Registrierungs-Verifizierung',
        'cooldown_3': 60,  # Stricter for signup!
        'cooldown_5': 120,
    },
}
```

### **Core Logic (DRY Principle)**
```python
# icon_challenge/engine.py

class IconChallengeEngine:
    def generate_challenge(self):
        """
        Generate 3×3 icon grid with count challenge.
        Returns: {icons, target_icon, correct_count, target_svg}
        """
        # 1. Pick 3 random icon types from 40-icon pool
        # 2. Choose target icon (will be counted)
        # 3. Add target 2-4 times
        # 4. Fill remaining with other icons
        # 5. Shuffle
        # 6. Store correct count in session
        
    def verify_attempt(self, user_count):
        """
        Verify user's answer with rate limiting.
        Returns: {success, message, blocked, wait_time}
        """
        # 1. Check rate limit
        # 2. Compare user_count with session['correct_count']
        # 3. Handle success/failure
        # 4. Generate new challenge on error
```

### **Multi-Layer Defense**

| Layer | Purpose | Effectiveness |
|-------|---------|---------------|
| **1. Honeypot** | Hidden field catches dumb bots | ~80% bot filter |
| **2. Icon-Challenge** | 20% success rate per attempt | ~30s per spam email |
| **3. Rate Limiting** | 3→30s, 5→60s cooldowns | Prevents brute force |
| **4. Silent Reset** | Reset to 1 (not 0) after cooldown | Better UX |
| **5. Email Verification** | Django-Allauth signup flow | Prevents fake accounts |

### **Integration Example: Contact Form**
```python
# core/views.py (OLD - WITHOUT Icon-Challenge)
@require_POST
def contact(request):
    # Direct email send - vulnerable to bots!
    send_email(...)
    
# NEW - WITH Icon-Challenge
@require_POST
def contact(request):
    # Step 1: Validate form
    # Step 2: Save data in session
    # Step 3: Trigger Icon-Challenge modal
    # Step 4: Email only sent AFTER challenge success
```
```html
<!-- contact.html -->
<form id="contact-form">
    <input name="name" required>
    <input name="email" required>
    <textarea name="message" required></textarea>
    
    <!-- Honeypot (invisible) -->
    <input type="text" name="website" style="display:none">
    
    <!-- Submit with HTMX -->
    <button type="button"
            hx-post="{% url 'icon_challenge:contact_prepare' %}"
            hx-include="#contact-form"
            hx-target="#contact-result">
        Send Message
    </button>
</form>

<div id="contact-result"></div>
```

---

## 🚀 **Quick Start**

### **Prerequisites**

- Python 3.12+
- PostgreSQL (optional, SQLite works for local dev)
- Git

### **1. Clone Repository**
```bash
git clone https://github.com/Martin-Frei/portfolio_site.git
cd portfolio_site
```

### **2. Create Virtual Environment**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Environment Variables**

Create `.env` file in project root:
```bash
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional, defaults to SQLite)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Cloudinary (for media storage)
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# Resend (for emails)
RESEND_API_KEY=re_xxxxxxxxxxxx
DEFAULT_FROM_EMAIL=noreply@yourdomain.com

# Google Gemini (for AI tips)
GEMINI_API_KEY=your-gemini-key

# Production
CSRF_TRUSTED_ORIGINS=https://yourdomain.com
```

### **5. Database Setup**
```bash
python manage.py migrate
python manage.py create_guest_user  # Creates guest account
python manage.py createsuperuser    # Create admin account
```

### **6. Run Development Server**
```bash
python manage.py runserver
```

Visit: **http://localhost:8000**

---

## 💻 **Local Development Setup**

### **Project Structure Deep-Dive**
```
portfolio_site/
├── portfolio_site/        # Main Django project
│   ├── settings.py        # Configuration
│   ├── urls.py            # Root URL routing
│   └── wsgi.py            # WSGI entry point
│
├── apps/                  # Django apps (see Architecture section)
│
├── static/                # Static files (CSS, JS, Images)
│   ├── css/
│   ├── js/
│   └── img/
│
├── media/                 # User uploads (local dev only)
│   └── projects/
│
├── templates/             # Global templates
│   ├── base.html          # Base template (nav, footer, scripts)
│   └── account/           # Django-Allauth templates
│
├── staticfiles/           # Collected static files (prod)
│
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (git-ignored)
├── .gitignore
├── manage.py              # Django management script
└── README.md              # This file
```

### **Common Management Commands**
```bash
# Database
python manage.py makemigrations
python manage.py migrate
python manage.py dbshell  # Access database

# Static Files
python manage.py collectstatic  # For production

# Custom Commands
python manage.py create_guest_user       # Setup guest account
python manage.py cleanup_loginlogs       # Remove logs >90 days

# Shell
python manage.py shell  # Django shell with models loaded
```

### **Development Workflow**

1. **Create Feature Branch**
```bash
   git checkout -b feature/your-feature-name
```

2. **Make Changes**
   - Edit code
   - Test locally
   - Check for errors

3. **Run Migrations** (if models changed)
```bash
   python manage.py makemigrations
   python manage.py migrate
```

4. **Commit & Push**
```bash
   git add .
   git commit -m "feat: add your feature"
   git push origin feature/your-feature-name
```

5. **Deploy** (Railway auto-deploys from main branch)
```bash
   git checkout main
   git merge feature/your-feature-name
   git push origin main
```

---

## 📦 **Tech Stack**

### **Backend**

| Technology | Version | Purpose |
|------------|---------|---------|
| **Django** | 5.1 | Web framework |
| **Python** | 3.12 | Programming language |
| **PostgreSQL** | Latest | Production database |
| **SQLite** | Built-in | Development database |
| **Gunicorn** | Latest | WSGI HTTP server |
| **Django-Allauth** | Latest | Authentication (Email verification) |
| **Whitenoise** | Latest | Static file serving |
| **python-decouple** | Latest | Environment variable management |
| **dj-database-url** | Latest | Database URL parsing |

### **Frontend**

| Technology | Version | Purpose |
|------------|---------|---------|
| **Tailwind CSS** | 3.x | Utility-first CSS framework |
| **HTMX** | 2.0 | Dynamic UI without JavaScript frameworks |
| **Lucide Icons** | Latest | SVG icon library (40 icons for challenge) |
| **Vanilla JavaScript** | ES6+ | Interactions (timer, dark mode, smooth scroll) |

### **External Services**

| Service | Purpose | Free Tier |
|---------|---------|-----------|
| **Cloudinary** | Media storage & CDN | 25 GB storage, 25 GB bandwidth/month |
| **Resend** | Transactional emails | 100 emails/day |
| **Google Gemini** | AI health tips | 60 requests/minute |
| **Railway** | PaaS hosting | $5 free credit/month |

### **Development Tools**

- **VS Code** - IDE
- **Git / GitHub** - Version control
- **Postman** - API testing
- **Railway CLI** - Deployment
- **PostgreSQL Client** - Database management

---

## 🌐 **Deployment**

### **Railway Deployment (Current)**

**Why Railway?**
- ✅ Auto HTTPS with Let's Encrypt
- ✅ Zero-downtime deploys
- ✅ Auto-scaling
- ✅ PostgreSQL add-on
- ✅ GitHub integration (auto-deploy on push)

### **Step-by-Step Deployment**

#### **1. Railway Setup**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link project
railway link
```

#### **2. Add PostgreSQL**

1. Railway Dashboard → New → Database → PostgreSQL
2. Copy `DATABASE_URL` to environment variables

#### **3. Environment Variables (Railway)**

Set in Railway Dashboard → Variables:
```
SECRET_KEY=<generate-new-secret>
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,.railway.app
DATABASE_URL=<auto-set-by-railway>
CSRF_TRUSTED_ORIGINS=https://yourdomain.com

# External APIs
CLOUDINARY_CLOUD_NAME=xxx
CLOUDINARY_API_KEY=xxx
CLOUDINARY_API_SECRET=xxx
RESEND_API_KEY=re_xxx
GEMINI_API_KEY=xxx
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

#### **4. Deploy**
```bash
# Manual deploy
railway up

# OR: Auto-deploy on git push
git push origin main  # Railway auto-deploys!
```

#### **5. Run Migrations (First Deploy)**
```bash
railway run python manage.py migrate
railway run python manage.py create_guest_user
railway run python manage.py createsuperuser
```

#### **6. Custom Domain**

1. Railway Dashboard → Settings → Domains
2. Add custom domain: `yourdomain.com`
3. Update DNS:
```
   Type: A
   Name: @
   Value: <railway-ip>
```
4. Wait for HTTPS (auto-generated by Railway)

### **Alternative: Docker Deployment**
```dockerfile
# Dockerfile (example for other platforms)
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

CMD gunicorn portfolio_site.wsgi:application --bind 0.0.0.0:$PORT
```

---

## 🔧 **Configuration**

### **Settings.py Structure**
```python
# portfolio_site/settings.py

# Security
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media Files (Cloudinary)
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Email (Resend API)
# Handled via requests library in views

# Context Processors (Guest Timer)
TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            # ... default processors
            'accounts.views.guest_timer',  # Custom!
        ],
    },
}]
```

### **Important Django Settings**
```python
# CSRF Protection
CSRF_TRUSTED_ORIGINS = [
    'https://martin-freimuth.dev',
    'https://*.railway.app',
]

# Session
SESSION_COOKIE_AGE = 86400  # 24 hours
SESSION_SAVE_EVERY_REQUEST = True

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
     'OPTIONS': {'min_length': 12}},  # Stronger than default!
]

# Django-Allauth
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
LOGIN_REDIRECT_URL = '/projects/'
```

---

## 📖 **API Documentation**

### **Icon-Challenge Endpoints**

#### **1. Start Challenge**
```http
GET /icon-challenge/start/<context_type>/
```

**Parameters:**
- `context_type`: `guest` | `contact` | `signup`

**Response:** HTML (Modal with 3×3 icon grid)

**Example:**
```html
<!-- Trigger via HTMX -->
<button hx-get="/icon-challenge/start/guest/"
        hx-target="#modal-container">
    Gast-Zugang
</button>
```

#### **2. Verify Challenge**
```http
POST /icon-challenge/verify/<context_type>/
```

**Parameters:**
- `context_type`: `guest` | `contact` | `signup`

**Body:**
```json
{
  "count": "3"
}
```

**Response:** HTML (Success/Error message)

**Rate Limiting:**
- 3 attempts → 30s cooldown (guest/contact)
- 5 attempts → 60s cooldown (guest/contact)
- Signup: 60s/120s (stricter)

#### **3. Prepare Forms** (Context-Specific)
```http
POST /icon-challenge/contact-prepare/
POST /icon-challenge/signup-prepare/
```

**Purpose:** Validate form data → Save to session → Trigger challenge

---

### **Resend API Integration**
```python
# core/views.py - Contact Form Example

import requests
from django.conf import settings

def send_contact_email(name, email, subject, message):
    """Send email via Resend API"""
    
    url = "https://api.resend.com/emails"
    headers = {
        "Authorization": f"Bearer {settings.RESEND_API_KEY}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "from": settings.DEFAULT_FROM_EMAIL,
        "to": "mat.frei@gmx.de",
        "subject": f"📬 Kontaktanfrage: {subject}",
        "reply_to": email,
        "text": f"From: {name}\nEmail: {email}\n\n{message}",
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=10)
    return response.ok
```

---

### **Gemini API Integration**
```python
# bmi_app/views.py

def ask_gemini_rest(prompt: str) -> str:
    """
    Call Google Gemini API without official SDK.
    Lightweight alternative to google-generativeai package.
    """
    
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {
        "x-goog-api-key": config("GEMINI_API_KEY"),
        "Content-Type": "application/json",
    }
    
    body = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=15)
    data = response.json()
    
    return data["candidates"][0]["content"]["parts"][0]["text"]
```

---

## 🧪 **Testing**

### **Manual Testing Checklist**
```bash
# Guest Login Flow
[ ] Click "Gast-Zugang"
[ ] Modal appears with 3×3 grid
[ ] Count target icons
[ ] Submit correct answer → Login successful
[ ] Submit wrong answer 3× → 30s cooldown
[ ] Timer counts down in nav
[ ] Auto-logout after 2 minutes

# Contact Form
[ ] Fill form
[ ] Submit → Icon-Challenge appears
[ ] Solve challenge → Email sent
[ ] Check inbox for confirmation

# Signup Flow
[ ] Fill registration form
[ ] Submit → Icon-Challenge appears
[ ] Solve challenge → Account created
[ ] Check inbox for verification email
[ ] Click verification link → Account activated

# Rate Limiting
[ ] Fail challenge 3× → 30s block
[ ] Fail challenge 5× → 60s block
[ ] Countdown timer visible
[ ] Silent reset after cooldown

# Honeypot
[ ] Fill hidden "website" field → Fake success (no email sent)
```

### **Unit Tests (Future)**
```python
# tests/test_icon_challenge.py (example)

from django.test import TestCase, Client
from icon_challenge.engine import IconChallengeEngine

class IconChallengeTests(TestCase):
    def setUp(self):
        self.client = Client()
        
    def test_challenge_generation(self):
        """Test 3×3 grid generation"""
        engine = IconChallengeEngine(self.client.request(), 'guest')
        challenge = engine.generate_challenge()
        
        self.assertEqual(len(challenge['icons']), 9)
        self.assertIn(challenge['target_icon'], [icon[0] for icon in challenge['icons']])
        
    def test_rate_limiting(self):
        """Test progressive rate limiting"""
        # Simulate 3 failed attempts
        for _ in range(3):
            response = self.client.post('/icon-challenge/verify/guest/', {'count': '0'})
        
        # 4th attempt should be blocked
        response = self.client.post('/icon-challenge/verify/guest/', {'count': '3'})
        self.assertContains(response, 'Warte noch')
```

---

## 🤝 **Contributing**

### **How to Contribute**

1. **Fork the Repository**
```bash
   # Click "Fork" on GitHub
   git clone https://github.com/YOUR-USERNAME/portfolio_site.git
```

2. **Create Feature Branch**
```bash
   git checkout -b feature/amazing-feature
```

3. **Make Changes**
   - Follow Django best practices
   - Keep code DRY (Don't Repeat Yourself)
   - Add docstrings to functions
   - Update README if needed

4. **Test Locally**
```bash
   python manage.py runserver
   # Test all affected features
```

5. **Commit & Push**
```bash
   git add .
   git commit -m "feat: add amazing feature"
   git push origin feature/amazing-feature
```

6. **Create Pull Request**
   - Describe changes
   - Link related issues
   - Request review

### **Code Style**

- **Python**: Follow PEP 8
- **Django**: Use Django's naming conventions
- **HTML/CSS**: Use Tailwind utility classes
- **JavaScript**: ES6+ syntax

### **Commit Message Convention**
```
feat: add new feature
fix: bug fix
docs: documentation update
style: formatting changes
refactor: code refactoring
test: add tests
chore: maintenance tasks
```

---

## 📄 **License**

This project is **open source** and available under the [MIT License](LICENSE).
```
MIT License

Copyright (c) 2025 Martin Freimuth

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📧 **Contact**

**Martin Freimuth** - Fullstack Developer

- **Portfolio**: [https://martin-freimuth.dev](https://martin-freimuth.dev)
- **Email**: mat.frei@gmx.de
- **LinkedIn**: [Martin Freimuth](https://www.linkedin.com/in/martin-freimuth-089249359/)
- **GitHub**: [@Martin-Frei](https://github.com/Martin-Frei)

---

## 🙏 **Acknowledgments**

- **Django Community** - Excellent documentation & ecosystem
- **Tailwind Labs** - Beautiful utility-first CSS framework
- **HTMX** - Making dynamic UIs simple again
- **Railway** - Best developer experience for deployment
- **Lucide Icons** - Beautiful open-source icon library

---

## 📊 **Project Stats**

- **Lines of Code**: ~2,500+
- **Django Apps**: 7
- **External APIs**: 3 (Cloudinary, Resend, Gemini)
- **Dependencies**: ~20 packages
- **Development Time**: 3+ months
- **Production Status**: ✅ Live & Stable

---

<div align="center">

**⭐ Star this repo if you find it helpful!**

**Built with ❤️ and lots of ☕ by Martin Freimuth**

</div>