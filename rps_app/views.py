from django.shortcuts import render
import json 
import random
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

# Kein globaler Context mehr!

def main(request):
    choices = [
        ('rock', 'Rock', 'Stein'),
        ('paper', 'Paper', 'Papier'),
        ('scissors', 'Scissors', 'Schere'),
    ]
    return render(request, 'rps/index.html', {'choices': choices})


# @require_http_methods(["POST"])
def game(request):
    # Session initialisieren
    if 'user_score' not in request.session:
        request.session['user_score'] = 0
        request.session['computer_score'] = 0
        request.session['draw_score'] = 0          # ← NEU

    try:
        data = json.loads(request.body)
        user = data.get('userChoice')
        choices = ['rock', 'paper', 'scissors']
        
        if user not in choices:
            return JsonResponse({'error': 'Invalid choice'}, status=400)
        
        computer_choice = random.choice(choices)
        
        if user == computer_choice:
            result = 'Unentschieden!'
            request.session['draw_score'] += 1                    # ← NEU: +1 bei Draw
        elif (user == 'rock' and computer_choice == 'scissors') or \
             (user == 'paper' and computer_choice == 'rock') or \
             (user == 'scissors' and computer_choice == 'paper'):
            result = 'Du gewinnst!'
            request.session['user_score'] += 1
        else:
            result = 'Computer gewinnt!'
            request.session['computer_score'] += 1
        
        request.session.modified = True
        
        return JsonResponse({
            'result': result,
            'user': request.session['user_score'],
            'draw': request.session['draw_score'],        # ← NEU: zurückgeben
            'computer': request.session['computer_score'],
            'computerChoice': computer_choice.capitalize()
        })
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def resetGame(request):
    request.session['user_score'] = 0
    request.session['computer_score'] = 0
    request.session['draw_score'] = 0           # ← NEU: auch Draw zurücksetzen
    request.session.modified = True
    return JsonResponse({
        'user': 0,
        'draw': 0,                              # ← NEU
        'computer': 0,
    })