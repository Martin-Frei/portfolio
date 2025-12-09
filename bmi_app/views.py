from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import json
import requests
from decouple import config


api_key = config('GEMINI_API_KEY')


def calculator(request):
    """BMI Calculator Hauptseite - umbenennen von 'main' zu 'calculator'"""
    return render(request, 'bmi/calculator.html')


@require_POST
def get_input(request):
    try:
        # Daten aus POST holen
        name = request.POST.get('name', 'Unbekannt')
        age = float(request.POST.get('age', 30))
        weight = float(request.POST.get('weight', 70))
        height = float(request.POST.get('height', 170))

        # BMI berechnen
        bmi = round(weight / ((height / 100) ** 2), 1)

        # Kategorie + Farbe
        if bmi < 18.5:
            category, color = "Untergewicht", "#f39c12"
        elif bmi < 25:
            category, color = "Normalgewicht", "#27ae60"
        elif bmi < 30:
            category, color = "Übergewicht", "#e67e22"
        else:
            category, color = "Adipositas", "#e74c3c"

        # Gemini aufrufen
        try:
            prompt = f"{name} ist {int(age)} Jahre alt, wiegt {weight}kg, ist {height}cm groß und hat einen BMI von {bmi} ({category}). Gib 4-5 motivierende Gesundheitstipps mit Ernährung und Sport. Direkt mit Tipps beginnen, kein Hallo."
            ai_tips = ask_gemini_rest(prompt)
        except Exception as e:
            ai_tips = f"Gemini nicht erreichbar: {str(e)}"

        # HTML zurückgeben
        html = f"""
        <div style="padding:30px; background:{color}20; border-left:6px solid {color}; border-radius:15px; font-family:sans-serif;">
            <h2 style="color:{color}">Hallo {name}!</h2>
            <p><strong>Dein BMI:</strong> {bmi} → <strong>{category}</strong></p>
            <p>Alter: {int(age)} | Gewicht: {weight}kg | Größe: {height}cm</p>
            <hr>
            <div style="background:white; padding:20px; border-radius:10px; margin-top:15px;">
                <strong>KI-Tipps für dich:</strong><br><br>
                {ai_tips.replace('\n', '<br>')}
            </div>
        </div>
        """
        return HttpResponse(html)

    except Exception as e:
        return HttpResponse(f"<div style='color:red; padding:20px; background:#fee;'>Fehler: {str(e)}</div>")

# @require_POST
# def get_input(request):
#     """HTMX Endpoint für BMI Berechnung mit Gemini AI"""
#     print('Get Input is called')
    
#     try:
        
#         # Check if data comes as JSON (from HTMX hx-vals)
#         if request.content_type == 'application/json':
#             data = json.loads(request.body)
#             height = float(data['height'])
#             weight = float(data['weight'])
#             name = data['name']
#             age = float(data['age'])
#         else:
#             # Fallback to POST data (HTMX sendet normalerweise POST)
#             height = float(request.POST['height'])
#             weight = float(request.POST['weight'])
#             name = request.POST['name']
#             age = float(request.POST['age'])
        
#         # Calculate BMI
#         bmi = round(weight / (height * height / 10000), 2)
        
#         # Determine BMI category
#         if bmi < 18.5:
#             category = "Untergewicht"
#             color = "#f39c12"
#         elif bmi < 25:
#             category = "Normalgewicht"
#             color = "#27ae60"
#         elif bmi < 30:
#             category = "Übergewicht"
#             color = "#e67e22"
#         else:
#             category = "Adipositas"
#             color = "#e74c3c"
        
#         # Create prompt for Gemini
#         prompt = (
#             f"The BMI of {name} (age {age}) is {bmi} ({category}). "
#             f"Give health tips including food and exercise routine. "
#             f"Make it motivational in maximum 5 lines. "
#             f"Start directly with tips, no greeting."
#         )
        
#         # Get AI response
#         try:
#             ai_tips = ask_gemini_rest(prompt)
#             print("API Key verwendet:", api_key[:10] + "..." if api_key else "KEIN KEY!")
#             print("Prompt:", prompt)
#         except Exception as e:
#             ai_tips = f"⚠️ AI-Tipps momentan nicht verfügbar. Fehler: {str(e)}"
        
#         # Return HTML for HTMX to inject
#         html = f"""
#         <div style="
#             padding: 20px;
#             background: {color}20;
#             border-left: 4px solid {color};
#             border-radius: 5px;
#         ">
#             <h3 style="color: {color}; margin-bottom: 10px;">
#                 Hallo {name}!
#             </h3>
#             <p style="font-size: 18px; margin-bottom: 10px;">
#                 <strong>Dein BMI:</strong> {bmi}
#             </p>
#             <p style="font-size: 16px; margin-bottom: 10px;">
#                 <strong>Kategorie:</strong> {category}
#             </p>
#             <p style="font-size: 14px; color: #666; margin-bottom: 15px;">
#                 <strong>Alter:</strong> {int(age)} Jahre | 
#                 <strong>Gewicht:</strong> {weight} kg | 
#                 <strong>Größe:</strong> {height} cm
#             </p>
#             <hr style="margin: 15px 0; border: none; border-top: 1px solid #ddd;">
#             <div style="
#                 padding: 15px;
#                 background: white;
#                 border-radius: 5px;
#                 font-size: 14px;
#                 line-height: 1.6;
#             ">
#                 <strong>🤖 KI-Gesundheitstipps:</strong><br><br>
#                 {ai_tips}
#             </div>
#         </div>
#         """
        
#         return HttpResponse(html)
    
#     except KeyError as e:
#         error_html = f"""
#         <div style="padding: 15px; background: #fee2e2; border-left: 4px solid #ef4444; border-radius: 5px;">
#             <p><strong>❌ Fehler:</strong> Feld fehlt: {str(e)}</p>
#             <p>Bitte fülle alle Felder aus!</p>
#         </div>
#         """
#         return HttpResponse(error_html)
    
#     except ValueError as e:
#         error_html = f"""
#         <div style="padding: 15px; background: #fee2e2; border-left: 4px solid #ef4444; border-radius: 5px;">
#             <p><strong>❌ Fehler:</strong> Ungültige Eingabe!</p>
#             <p>Bitte gib nur Zahlen ein.</p>
#         </div>
#         """
#         return HttpResponse(error_html)
    
#     except Exception as e:
#         error_html = f"""
#         <div style="padding: 15px; background: #fee2e2; border-left: 4px solid #ef4444; border-radius: 5px;">
#             <p><strong>❌ Fehler:</strong> {str(e)}</p>
#         </div>
#         """
#         return HttpResponse(error_html)


def ask_gemini_rest(prompt: str, model: str = "gemini-2.0-flash-exp") -> str:
    """
    Ruft Google Gemini API auf und gibt Antwort zurück – mit Fehlerbehandlung!
    """
    api_key = config('GEMINI_API_KEY', default=None)
    
    if not api_key:
        return "Gemini API-Key fehlt. Bitte in Render Environment Variables eintragen."
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    
    body = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        resp = requests.post(url, headers=headers, json=body, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Gemini nicht erreichbar: {str(e)}"