# 🚀 Martin Freimuth - Portfolio Website

> Professional Django-based portfolio with custom authentication, modern UI & email verification

[![Django](https://img.shields.io/badge/Django-5.1-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.0-38bdf8.svg)](https://tailwindcss.com/)
[![Railway](https://img.shields.io/badge/Deployed-Railway-blueviolet.svg)](https://railway.app/)

## ✨ Features

### 🔐 Authentication & Security
- **Custom Icon-Challenge System** - CAPTCHA-Alternative für bessere UX
- **Email Verification** - Django-Allauth mit Resend API
- **Guest Access** - 2-Minuten Trial mit Auto-Logout Timer
- **Styled Confirmation Pages** - Alle Auth-Seiten im Portfolio-Design

### 🎨 User Experience
- **User Subnav** - 7 Navigation-Buttons für eingeloggte User
- **Mobile Menu** - 2-Spalten Layout mit Hamburger Toggle
- **Guest Timer** - Live-Countdown in Navbar (Desktop) und Header (Mobile)
- **Dark/Light Mode** - System-Preference + Manual Toggle
- **Responsive Design** - Mobile-First mit Tailwind CSS

### 📧 Email System
- **Resend API** - Custom Backend statt SMTP (schneller & zuverlässiger)
- **Dual Email Strategy** - noreply@ für System, hi@ für persönlich
- **Contact Form** - HTMX-powered mit Success-Messages

### 🎯 Projects
- **Public Showcase** - Öffentliche Projekt-Liste
- **Secret Lab** - Exklusive Projekte für eingeloggte User
- **Category Filtering** - Nach Tech-Stack filterbar
- **Cloudinary CDN** - Optimierte Bild-Auslieferung

### 📱 Mobile Optimization
- **2-Column Mobile Menu** - Main Nav + Subnav Pills
- **Touch-Optimized** - Große Touch-Targets, intuitive Navigation
- **Theme Toggle in Header** - Dark Mode auch mobil
- **Sticky Navigation** - Navbar + Subnav zusammen fixiert

## 🛠️ Tech Stack

### Backend
- **Django 5.1+** - Web Framework
- **PostgreSQL** - Database (Railway)
- **Django-Allauth** - Authentication
- **Resend API** - Email Service
- **Cloudinary** - Media Storage

### Frontend
- **Tailwind CSS** - Utility-First CSS
- **HTMX** - Dynamic UI ohne JavaScript-Framework
- **Vanilla JavaScript** - Für Interaktionen
- **Responsive Design** - Mobile-First Approach

### Deployment
- **Railway** - Hosting (Backend + PostgreSQL)
- **Cloudinary** - CDN für Media Files
- **Custom Domain** - martin-freimuth.dev
- **Environment Variables** - Sichere Konfiguration

## 📦 Installation

### Prerequisites
```bash
Python 3.11+
PostgreSQL
Resend API Key
Cloudinary Account
```

### Setup

1. **Clone Repository**
```bash
git clone https://github.com/Martin-Frei/portfolio.git
cd portfolio
```

2. **Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. **Dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Variables (.env)**
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=postgresql://user:pass@localhost/portfolio
RESEND_API_KEY=re_xxxxxxxxxxxxx
DEFAULT_FROM_EMAIL=noreply@martin-freimuth.dev
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret
```

5. **Database Setup**
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. **Create Guest User**
```bash
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.create_user(username='guest', email='guest@example.com', password='guest123')
>>> exit()
```

7. **Run Development Server**
```bash
python manage.py runserver
```

Visit: `http://localhost:8000`

## 📁 Project Structure
```
portfolio/
├── accounts/              # User authentication & profiles
├── core/                  # Homepage, about, contact, skills
├── projects/              # Project showcase (public + secret)
├── icon_challenge/        # Custom CAPTCHA system
├── legal/                 # Impressum, Datenschutz
├── bmi_app/              # BMI Calculator (example project)
├── rps_app/              # Rock-Paper-Scissors (example)
├── portfolio_site/        # Main settings & config
├── templates/
│   ├── base.html         # Base template
│   ├── partials/         # Reusable components
│   │   ├── navbar.html
│   │   ├── footer.html
│   │   └── user_subnav.html
│   ├── account/          # Django-Allauth overrides
│   └── core/             # Core app templates
├── static/               # Static files
├── media/                # User uploads (dev only)
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Deployment (Railway)

### Railway Setup
1. Connect GitHub repository
2. Add PostgreSQL plugin
3. Set environment variables:
```
   SECRET_KEY
   DEBUG=False
   RESEND_API_KEY
   CLOUDINARY_CLOUD_NAME
   CLOUDINARY_API_KEY
   CLOUDINARY_API_SECRET
   ALLOWED_HOSTS=martin-freimuth.dev,*.railway.app
```
4. Deploy automatically on push

### Domain Setup
1. Add custom domain in Railway
2. Update DNS records (CNAME)
3. SSL automatically provisioned

## 🔮 Roadmap

- [ ] **Current Project Page** - Live-Progress meines Hauptprojekts
- [ ] **Next Ideas / Roadmap** - Geplante Features mit Voting-System
- [ ] **Interactive CV** - Timeline, Skills-Visualisierung, PDF-Download
- [ ] **IT Blog** - Tech-Artikel, Tutorials, Learnings
- [ ] **Training Area** - Coding-Challenges, Quiz, Lern-Tools
- [ ] **Project Analytics** - Visitor-Stats, beliebte Projekte
- [ ] **Multi-Language** - Deutsch/English Toggle

## 📸 Screenshots

*Coming soon*

## 🤝 Contributing

Dies ist ein persönliches Portfolio-Projekt. Feedback und Vorschläge sind willkommen!

## 📝 License

Private Project - All Rights Reserved

## 👤 Author

**Martin Freimuth**
- 📍 Location: Rosenheim, Bayern, Deutschland
- 📧 Email: mat.frei@gmx.de
- 💼 LinkedIn: [martin-freimuth-089249359](https://linkedin.com/in/martin-freimuth-089249359/)
- 🐙 GitHub: [@Martin-Frei](https://github.com/Martin-Frei)
- 🌐 Website: [martin-freimuth.dev](https://martin-freimuth.dev)

---

**Built with Django, Tailwind CSS, blood & caffeine** ☕💻

*Developer Akademie Graduate (März 2026) - Career Changer with 20+ years business experience*