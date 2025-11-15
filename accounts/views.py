from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

# Create your views here.


def register(request):                                          # View-Funktion für User-Registrierung (request enthält alle Infos über die HTTP-Anfrage)
    if request.method == 'POST':                                # Prüfen: Hat User das Formular ABGESCHICKT? (POST = Daten wurden gesendet)
        form = CustomUserCreationForm(request.POST)             # Form-Objekt erstellen MIT den eingegebenen Daten aus dem Formular
        if form.is_valid():                                     # Validierung: Sind alle Eingaben korrekt? (Email-Format, Username frei, Passwort stark genug, etc.)
            user = form.save()                                  # User in Datenbank speichern (ruft save() Methode aus forms.py auf)
            login(request, user)                                # User automatisch einloggen (Session wird erstellt, User muss sich nicht nochmal anmelden)
            return redirect('core:home')                        # Weiterleitung zur Homepage (Funktion endet hier, kein Code danach wird ausgeführt)
    else:                                                       # Wird ausgeführt wenn request.method == 'GET' (User öffnet die Seite zum ersten Mal)
        form = CustomUserCreationForm()                         # Leeres Form erstellen (ohne Daten, User sieht leere Eingabefelder)
    
    return render(request, 'accounts/register.html', {'form': form})  # Template rendern: Zeige register.html mit dem Form (leer bei GET, mit Fehlern bei POST+invalid)

'''
# Registration View - Wie funktioniert die Fehlerbehandlung?

## 📝 Die komplette views.py mit Kommentaren

```python
# Django Shortcuts importieren: render (Template anzeigen) und redirect (Weiterleitung)
from django.shortcuts import render, redirect
# Django's Login-Funktion importieren (loggt User nach Registration automatisch ein)
from django.contrib.auth import login
# Unser eigenes Registration-Form importieren (aus forms.py)
from .forms import CustomUserCreationForm

# Create your views here.



```

---

## 🎯 Wie bekommt der User die Fehlermeldungen zu sehen?

### Der Ablauf bei fehlerhafter Eingabe:

**1. User füllt falsch aus:**
```
Username: martin  (schon vergeben!)
Email: test@test.de
Password: 123  (zu kurz!)
```

**2. POST Request wird gesendet:**
```python
if request.method == 'POST':  # ✅ True
    form = CustomUserCreationForm(request.POST)  # Form mit Daten erstellen
```

**3. Validierung schlägt fehl:**
```python
if form.is_valid():  # ❌ False!
    # Dieser Block wird ÜBERSPRUNGEN
    # kein user = form.save()
    # kein login()
    # kein return redirect()
```

**4. Code läuft weiter bis zum Ende:**
```python
return render(request, 'accounts/register.html', {'form': form})
```

**5. Das Form-Objekt enthält jetzt die Fehler:**
```python
form.errors = {
    'username': ['Ein Benutzer mit diesem Namen existiert bereits.'],
    'password1': ['Das Passwort muss mindestens 8 Zeichen enthalten.']
}
```

**6. Im Template werden die Fehler angezeigt:**
```html
{{ form.username }}          <!-- Eingabefeld -->
{{ form.username.errors }}   <!-- ⚠️ Fehlermeldung erscheint hier! -->
```

---

## 📊 Die 3 Szenarien visualisiert:

### Szenario A: Seite öffnen (GET)
```
User → /accounts/register/
↓
request.method = 'GET'
↓
else: form = CustomUserCreationForm()  (leer)
↓
render Template mit leerem Form
↓
User sieht: [____] [____] [____]  (leere Felder)
```

### Szenario B: Falsche Eingabe (POST + invalid)
```
User → Füllt aus: Username "martin" (vergeben!)
↓
request.method = 'POST'
↓
form = CustomUserCreationForm(request.POST)
↓
form.is_valid() = False  (Username existiert!)
↓
form.errors = {'username': ['Existiert bereits']}
↓
return render mit Form (MIT Fehlern!)
↓
User sieht: 
[martin] ⚠️ Ein Benutzer mit diesem Namen existiert bereits.
[_____]
[_____]
```

### Szenario C: Korrekte Eingabe (POST + valid)
```
User → Füllt aus: Alles korrekt!
↓
request.method = 'POST'
↓
form = CustomUserCreationForm(request.POST)
↓
form.is_valid() = True ✅
↓
user = form.save()  (User erstellt!)
↓
login(request, user)  (Eingeloggt!)
↓
return redirect('core:home')  (Funktion endet HIER!)
↓
User sieht: Homepage (eingeloggt!)
```

---

## 🌍 Deutsche Fehlermeldungen aktivieren

### In `portfolio_site/settings.py` ändern:

```python
# Vorher:
LANGUAGE_CODE = 'en-us'

# Nachher:
LANGUAGE_CODE = 'de-de'
```

### Was wird übersetzt?

**Automatisch auf Deutsch:**
- ✅ Alle Django-Fehlermeldungen
- ✅ Admin-Interface
- ✅ Datum/Zeit-Formate
- ✅ Form-Validierungen
- ✅ Pagination

**NICHT automatisch übersetzt:**
- ❌ Deine eigenen Texte im Template
- ❌ Deine custom Fehlermeldungen (müssen manuell auf Deutsch geschrieben werden)

### Beispiel: Englisch vs Deutsch

**Mit `LANGUAGE_CODE = 'en-us'`:**
```
⚠️ A user with that username already exists.
⚠️ This field is required.
⚠️ Enter a valid email address.
⚠️ The two password fields didn't match.
```

**Mit `LANGUAGE_CODE = 'de-de'`:**
```
⚠️ Ein Benutzer mit diesem Benutzernamen existiert bereits.
⚠️ Dieses Feld ist erforderlich.
⚠️ Geben Sie eine gültige E-Mail-Adresse ein.
⚠️ Die zwei Passwortfelder stimmten nicht überein.
```

---

## 🎨 Wie Fehler im Template angezeigt werden (Vorschau)

```html
<!-- accounts/register.html (erstellen wir als nächstes) -->

<form method="post">
    {% csrf_token %}
    
    <!-- Username Feld -->
    {{ form.username.label_tag }}
    {{ form.username }}
    {% if form.username.errors %}
        <div class="error">
            {{ form.username.errors }}  <!-- ⚠️ Fehlermeldung erscheint HIER! -->
        </div>
    {% endif %}
    
    <!-- Email Feld -->
    {{ form.email.label_tag }}
    {{ form.email }}
    {% if form.email.errors %}
        <div class="error">
            {{ form.email.errors }}  <!-- ⚠️ Fehlermeldung erscheint HIER! -->
        </div>
    {% endif %}
    
    <button type="submit">Registrieren</button>
</form>
```

---

## ✅ Zusammenfassung: Der Flow

**Backend (views.py):**
```python
form.is_valid()  # ❌ False
# Form behält die Eingaben UND die Fehler
return render(..., {'form': form})  # Form mit Fehlern ans Template
```

**Template (register.html):**
```html
{{ form.username.errors }}  <!-- Django zeigt Fehler automatisch an! -->
```

**User sieht:**
```
⚠️ Ein Benutzer mit diesem Namen existiert bereits.
```

---

## 🚀 Nächste Schritte:

1. ✅ `LANGUAGE_CODE = 'de-de'` in settings.py setzen
2. ➡️ `accounts/urls.py` erstellen (NÄCHSTER SCHRITT)
3. ➡️ `accounts/templates/accounts/register.html` erstellen
4. ➡️ URLs in `portfolio_site/urls.py` einbinden
5. ➡️ Testen!

---

## 📋 Wichtige Dateien bis jetzt:

```
accounts/
├── forms.py          ✅ FERTIG (CustomUserCreationForm)
├── views.py          ✅ FERTIG (register View)
├── urls.py           ⏳ KOMMT ALS NÄCHSTES
└── templates/        ⏳ DANACH
    └── accounts/
        └── register.html
```
'''