"""
Icon-Challenge Engine
Core Logic für Challenge-Generierung und Verifizierung
"""

import random
import time
from .config import ICON_POOL, CHALLENGE_CONTEXTS


class IconChallengeEngine:
    """
    Zentrale Engine für Icon-Challenge System
    """
    
    def __init__(self, request, context_type):
        """
        Initialize Engine
        
        Args:
            request: Django Request-Objekt
            context_type: 'guest', 'contact', oder 'signup'
        """
        self.request = request
        self.context_type = context_type
        self.config = CHALLENGE_CONTEXTS[context_type]
        
        # Session-Keys (eindeutig pro Context)
        self.session_prefix = f'icon_challenge:{context_type}'
    
    
    def generate_challenge(self):
        """
        Generiere neue Challenge (3×3 Grid mit Count-Aufgabe)
        
        Returns:
            dict: {
                'icons': [(name, svg), ...],  # 9 Icons für Grid
                'target_icon': 'heart',       # Welches Icon zählen?
                'correct_count': 3,           # Wie oft kommt es vor?
                'target_svg': '<svg>...',     # SVG des Target-Icons
            }
        """
        grid_size = self.config['grid_size']  # 9
        min_count = self.config['min_count']  # 2
        max_count = self.config['max_count']  # 4
        
        # 1. Wähle 3 verschiedene Icon-Typen aus Pool
        icon_names = list(ICON_POOL.keys())
        selected_types = random.sample(icon_names, 3)
        
        # 2. Wähle eines als Target (das gezählt wird)
        target_icon = random.choice(selected_types)
        
        # 3. Bestimme, wie oft Target vorkommt (2-4)
        correct_count = random.randint(min_count, max_count)
        
        # 4. Erstelle Icon-Liste
        icons = []
        
        # Füge Target-Icons hinzu
        for _ in range(correct_count):
            icons.append(target_icon)
        
        # Fülle Rest mit anderen Icons auf
        other_icons = [icon for icon in selected_types if icon != target_icon]
        while len(icons) < grid_size:
            icons.append(random.choice(other_icons))
        
        # 5. Shuffle (damit Target nicht immer oben links ist)
        random.shuffle(icons)
        
        # 6. Konvertiere zu (name, svg) Tupeln
        icons_with_svg = [(name, ICON_POOL[name]) for name in icons]
        
        # 7. Speichere in Session
        self.request.session[f'{self.session_prefix}:target'] = target_icon
        self.request.session[f'{self.session_prefix}:count'] = correct_count
        self.request.session[f'{self.session_prefix}:icons'] = icons
        
        return {
            'icons': icons_with_svg,
            'target_icon': target_icon,
            'correct_count': correct_count,
            'target_svg': ICON_POOL[target_icon],
        }
    
    
    def verify_attempt(self, user_count):
        """
        Verifiziere User-Antwort + Rate Limiting
        
        Args:
            user_count: int - Vom User gewählte Anzahl
            
        Returns:
            dict: {
                'success': True/False,
                'message': 'Korrekt!' oder Fehlermeldung,
                'blocked': True/False (Rate Limit aktiv?),
                'wait_time': 30 (Sekunden warten),
            }
        """
        # 1. Rate Limiting prüfen
        rate_limit = self._check_rate_limit()
        if rate_limit['blocked']:
            return rate_limit
        
        # 2. Korrekte Antwort aus Session holen
        correct_count = self.request.session.get(f'{self.session_prefix}:count')
        
        if correct_count is None:
            return {
                'success': False,
                'message': 'Session abgelaufen. Bitte neu starten.',
                'blocked': False,
            }
        
        # 3. Vergleichen
        if int(user_count) == correct_count:
            # ✅ KORREKT!
            self._reset_attempts()
            return {
                'success': True,
                'message': '✅ Korrekt! Zugang gewährt.',
                'blocked': False,
            }
        else:
            # ❌ FALSCH!
            self._increment_attempts()
            attempts = self.request.session.get(f'{self.session_prefix}:attempts', 0)
            
            # Neue Challenge generieren für nächsten Versuch
            self.generate_challenge()
            
            return {
                'success': False,
                'message': f'❌ Falsch! Versuch {attempts}/5',
                'blocked': False,
            }
    
    
    def _check_rate_limit(self):
        """
        Prüfe Rate Limiting (3→30s, 5→60s)
        
        Returns:
            dict: {'blocked': True/False, 'wait_time': seconds, ...}
        """
        attempts = self.request.session.get(f'{self.session_prefix}:attempts', 0)
        last_attempt = self.request.session.get(f'{self.session_prefix}:last_attempt', 0)
        current_time = time.time()
        time_passed = current_time - last_attempt
        
        # Cooldown-Zeiten aus Config
        cooldown_3 = self.config['cooldown_3']  # 30s (guest/contact), 60s (signup)
        cooldown_5 = self.config['cooldown_5']  # 60s (guest/contact), 120s (signup)
        
        # Cooldown 30s/60s nach 3 Versuchen
        if attempts >= 3 and time_passed < cooldown_3:
            remaining = int(cooldown_3 - time_passed)
            return {
                'blocked': True,
                'success': False,
                'message': f'⏱️ Zu viele Versuche! Bitte warte {remaining} Sekunden.',
                'wait_time': remaining,
                'level': 'warning',
            }
        
        # Cooldown 60s/120s nach 5 Versuchen
        if attempts >= 5 and time_passed < cooldown_5:
            remaining = int(cooldown_5 - time_passed)
            return {
                'blocked': True,
                'success': False,
                'message': f'🚫 Maximale Versuche erreicht! Bitte warte {remaining} Sekunden.',
                'wait_time': remaining,
                'level': 'danger',
            }
        
        # Silent Reset nach Cooldown
        if time_passed >= cooldown_3 and attempts >= 3:
            self.request.session[f'{self.session_prefix}:attempts'] = 1
        
        return {'blocked': False}
    
    
    def _increment_attempts(self):
        """Erhöhe Fehlversuch-Counter"""
        attempts = self.request.session.get(f'{self.session_prefix}:attempts', 0)
        self.request.session[f'{self.session_prefix}:attempts'] = attempts + 1
        self.request.session[f'{self.session_prefix}:last_attempt'] = time.time()
    
    
    def _reset_attempts(self):
        """Reset Counter (nach erfolgreichem Versuch)"""
        self.request.session[f'{self.session_prefix}:attempts'] = 0
        self.request.session[f'{self.session_prefix}:last_attempt'] = 0
    
    
    def cleanup(self):
        """
        Räume Session auf (nach erfolgreichem Login)
        """
        keys_to_delete = [
            f'{self.session_prefix}:target',
            f'{self.session_prefix}:count',
            f'{self.session_prefix}:icons',
            f'{self.session_prefix}:attempts',
            f'{self.session_prefix}:last_attempt',
        ]
        
        for key in keys_to_delete:
            self.request.session.pop(key, None)


# ============================================
# HELPER FUNCTIONS (für einfache Usage)
# ============================================

def generate_challenge(request, context_type):
    """
    Shortcut: Generiere Challenge
    
    Usage:
        challenge = generate_challenge(request, 'guest')
    """
    engine = IconChallengeEngine(request, context_type)
    return engine.generate_challenge()


def verify_challenge(request, context_type, user_count):
    """
    Shortcut: Verifiziere Challenge
    
    Usage:
        result = verify_challenge(request, 'guest', user_count=3)
        if result['success']:
            # Login User
    """
    engine = IconChallengeEngine(request, context_type)
    return engine.verify_attempt(user_count)


def cleanup_challenge(request, context_type):
    """
    Shortcut: Cleanup Session
    
    Usage:
        cleanup_challenge(request, 'guest')
    """
    engine = IconChallengeEngine(request, context_type)
    engine.cleanup()