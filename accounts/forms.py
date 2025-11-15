from django import forms                                            # Django Form-System importieren
from django.contrib.auth.models import User                         # Django's eingebautes User-Model importieren
from django.contrib.auth.forms import UserCreationForm              # Django's vorgefertigtes Registration-Formular importieren


class CustomUserCreationForm(UserCreationForm):                     # Erbt von UserCreationForm alle Felder (username, password1, password2)
    email = forms.EmailField(required=True)                         # Zusätzliches Feld email (Pflichtfeld)
    
    class Meta:                                                     # Meta-Klasse: Konfiguration über die Form
        model = User                                                # Model ist User (speichert in auth_user Tabelle)
        fields = ['username', 'email', 'password1', 'password2']    # Felder, die im Formular angezeigt werden sollen (in dieser Reihenfolge)
        
        
    def clean_email(self):                                          # Validierungs-Methode für Email (wird automatisch von Django aufgerufen)
        email = self.cleaned_data.get('email')                      # Hole die eingegebene Email aus den validierten Daten
        if User.objects.filter(email=email).exists():               # Prüfe: Existiert bereits ein User mit dieser Email?
            raise forms.ValidationError("Diese Email-Adresse wird bereits verwendet.")  # Wenn JA: Fehlermeldung anzeigen
        return email                                                # Wenn NEIN: Email ist gültig, gib sie zurück
        
    def save(self, commit=True):                                    # Überschreibt die save-Methode (damit Email auch gespeichert wird)
        user = super().save(commit=False)                           # Rufe Original-save() auf, aber speichere noch NICHT in DB (commit=False)
        user.email = self.cleaned_data['email']                     # Setze die Email im User-Objekt (sonst würde sie ignoriert)
        if commit:                                                  # Wenn commit=True (Standard):
            user.save()                                             # Jetzt User in Datenbank speichern (mit username, password UND email)
        return user                                                 # User-Objekt zurückgeben (damit andere Code-Teile es nutzen können)