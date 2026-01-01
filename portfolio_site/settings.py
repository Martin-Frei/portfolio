"""
Django settings for portfolio_site project – FINAL PRODUCTION READY VERSION
"""

from pathlib import Path
import os
from decouple import config
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ==================== SECURITY & ENV ====================
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    ".railway.app",
    "martin-freimuth.dev",
    "www.martin-freimuth.dev",  # falls jemand www benutzt
]

# CSRF für Railway + Custom Domain
CSRF_TRUSTED_ORIGINS = [
    "https://*.railway.app",
    "https://martin-freimuth.dev",
    "https://www.martin-freimuth.dev",
]

# Production Security (nur wenn DEBUG = False)
if not DEBUG:
    # SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

    # HSTS – grünes Schloss + extra Sicherheit
    SECURE_HSTS_SECONDS = 31536000  # 1 Jahr
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# ==================== APPLICATIONS ====================
INSTALLED_APPS = [
    "cloudinary_storage",  # MUSS vor django.contrib.staticfiles!
    
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    
    "cloudinary",
    
    # ========== TAGGIT (NEU!) ==========
    "taggit",
    "taggit_autosuggest",
    # ===================================
    
    # Deine Apps:
    "core",
    "projects",
    "accounts",
    "legal",
    "bmi_app",
    "rps_app",
    "icon_challenge",
    
    # Allauth (am Ende):
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
]


'''
## 🎯 **WARUM DIESE REIHENFOLGE?**

1. cloudinary_storage    ← VOR staticfiles (Override!)
2. Django Core Apps      ← Standard Django
3. cloudinary            ← Nach Core
4. taggit + autosuggest  ← VOR deinen Apps! ✅
5. Deine Apps            ← Können taggit nutzen
6. allauth               ← Am Ende (Templates Override)

---

## ⚠️ **KRITISCH:**

FALSCH ❌:
core
projects
taggit  ← Zu spät!

RICHTIG ✅:
taggit
taggit_autosuggest
core    ← Kann jetzt taggit in models.py importieren!
projects

'''

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

WHITENOISE_USE_FINDERS = True
WHITENOISE_MANIFEST_STRICT = False

ROOT_URLCONF = "portfolio_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'accounts.views.guest_timer',
            ],
        },
    },
]

WSGI_APPLICATION = "portfolio_site.wsgi.application"

# ==================== DATABASE ====================
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ==================== PASSWORD VALIDATION ====================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==================== INTERNATIONALIZATION ====================
LANGUAGE_CODE = "de-de"
TIME_ZONE = "Europe/Berlin"
USE_I18N = True
USE_TZ = True

# ==================== STATIC & MEDIA ====================
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
MEDIA_URL = "/media/"
MEDIA_ROOT = '/app/media' 

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cloudinary Credentials
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': config('CLOUDINARY_NAME'),
    'API_KEY': config('CLOUDINARY_API_KEY'),
    'API_SECRET': config('CLOUDINARY_API_SECRET'),
}

# Geänderter Block: Wir nutzen jetzt das Standard-Storage für Static Files
# Das verhindert den "FileNotFoundError" beim Deployment auf Railway
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Wichtig für die Cloudinary-Library Kompatibilität (Legacy-Variablen)
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"


# ==================== ALLAUTH ====================
SITE_ID = 1

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https" if not DEBUG else "http"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

LOGIN_REDIRECT_URL = "/projects/secret-lab/"
LOGOUT_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
ACCOUNT_SESSION_REMEMBER = None
ACCOUNT_SIGNUP_OPEN = True  # Fremde können sich registrieren
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

SESSION_COOKIE_AGE = 86400
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# ==================== E-MAIL (RESEND API) ====================
if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    # API STATT SMTP 
    EMAIL_BACKEND = "portfolio_site.email_backend.ResendAPIBackend"

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="noreply@martin-freimuth.dev")
SERVER_EMAIL = DEFAULT_FROM_EMAIL
RESEND_API_KEY = config("RESEND_API_KEY")