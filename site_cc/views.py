from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
import requests
import google.generativeai as genai
from django.shortcuts import render
from datetime import datetime, timedelta
from django.shortcuts import render
from calendar import monthrange
import datetime
from .models import Evento
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Evento
import json
import datetime
import calendar
import os
from gtts import gTTS
from datetime import datetime
import requests
from django.shortcuts import render

API_KEY = 'AIzaSyC4AVfey0X8ONDz9f_vdw6Sq9yDdhHFowk'
genai.configure(api_key=API_KEY)

plantas = {
    'Tomate': {
        'se_da_bem': ['Cenoura', 'Alface'],
        'nao_se_da_bem': ['Batata'],
        'indiferente': ['Rúcula'],
    },
    'Cenoura': {
        'se_da_bem': ['Alface', 'Rúcula'],
        'nao_se_da_bem': ['Batata'],
        'indiferente': ['Tomate'],
    },
    'Alface': {
        'se_da_bem': ['Cenoura', 'Rúcula'],
        'nao_se_da_bem': ['Batata'],
        'indiferente': ['Tomate'],
    },
    'Batata': {
        'se_da_bem': ['Rúcula'],
        'nao_se_da_bem': ['Tomate', 'Cenoura'],
        'indiferente': ['Alface'],
    },
    'Rúcula': {
        'se_da_bem': ['Cenoura', 'Alface'],
        'nao_se_da_bem': ['Batata'],
        'indiferente': ['Tomate'],
    },
}

def pagina_principal(request):
    resultado = None
    texto_gerado = None
    planta = request.GET.get('planta')

    print(f"Planta selecionada: {planta}")

    if planta:
        planta = planta.capitalize()
        if planta in plantas:
            resultado = plantas[planta]

            prompt_fixo = """
            Você só pode falar sobre agronomia, sustentabilidade, práticas agrícolas, tipos de solo e plantio. 
            Não quero que fuja para temas paralelos, como sugestões de vídeos ou coisas do tipo. Quero que tudo que for sugerir ou responder envolva apenas texto.
            Se a pergunta não tiver nada sobre agricultura ou algo relacionado, responda com: 
            'Não posso responder sobre esse tema, fui treinado apenas para práticas agrícolas.'
            """

            prompt_geracao = f"Escreva um texto de 2 linhas onde fala sobre {planta}, incluindo informações sobre sua compatibilidade com estas plantas, explicando o motivo da compatibilidade {plantas}"

            try:
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt_geracao)
                texto_gerado = response.text.strip()

                if 'Não posso responder' in texto_gerado:
                    texto_gerado = "Nenhuma informação válida gerada sobre a planta."
            except Exception as e:
                print(f"Erro ao gerar texto: {e}")

    contexto = {
        'plantas': plantas.keys(),
        'planta': planta,
        'resultado': resultado,
        'texto_gerado': texto_gerado if texto_gerado else "Nenhum texto gerado pela IA.",
    }

    return render(request, 'pagina_principal.html', contexto)

def introducao(request):
    return render(request, 'introducao.html')

def equipe(request):
    return render(request, 'equipe.html')

def contato(request):
    return render(request, 'contato.html')

def calendario(request):
    return render(request, 'calendario.html')


def tempo(request):
    API_KEY = "ae959f54e6804eb49fd210633242409"
    cidade = "Carpina"
    
    link_forecast = f"http://api.weatherapi.com/v1/forecast.json?key={API_KEY}&q={cidade}&days=7&lang=pt"
    
    try:
        requisicao_forecast = requests.get(link_forecast)
        requisicao_forecast.raise_for_status()
        requisicao_forecast_dic = requisicao_forecast.json()

        if "forecast" not in requisicao_forecast_dic:
            contexto = {'erro': 'Não foi possível obter a previsão do tempo.'}
        else:
            previsao = []
            cidade_info = {
                'nome': requisicao_forecast_dic['location']['name'],
            }

            
            today = datetime.now().date().strftime("%Y-%m-%d")

            for item in requisicao_forecast_dic['forecast']['forecastday']:
                previsao.append({
                    'data': item['date'],
                    'descricao': item['day']['condition']['text'],
                    'temperatura_max': item['day']['maxtemp_c'],
                    'temperatura_min': item['day']['mintemp_c'],
                    'umidade': item['day']['avghumidity'],
                    'precipitacao': item['day']['totalprecip_mm'],
                    'vento_velocidade': item['day']['maxwind_kph'],
                })

            contexto = {
                'cidade': cidade_info,
                'previsao': previsao,
                'today': today  
            }

    except requests.exceptions.RequestException as e:
        contexto = {
            'erro': f"Erro ao fazer a requisição: {e}"
        }
    
    return render(request, 'tempo.html', contexto)


class HomePageView(ListView):
    template_name = 'pagina_principal.html'
    ordering = ['-dataDeCriacao']

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Você está logado.")
            return redirect('pagina_principal')
        else:
            messages.error(request, "Ocorreu um erro. Tente novamente.")
            return redirect('login')
    return render(request, 'login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "Você saiu.")
    return redirect('pagina_principal')

from calendar import monthcalendar

def calendario(request, year=None, month=None):
    today = datetime.date.today()
    current_year = year if year else today.year
    current_month = month if month else today.month

    first_day_of_month = datetime.date(current_year, current_month, 1)
    _, last_day_of_month = calendar.monthrange(current_year, current_month)
    first_weekday = first_day_of_month.weekday()
    days = list(range(1, last_day_of_month + 1))
    empty_days = [None] * (first_weekday + 1 if first_weekday != 6 else 0)

    if current_month == 1:
        prev_month, prev_year = 12, current_year - 1
    else:
        prev_month, prev_year = current_month - 1, current_year

    if current_month == 12:
        next_month, next_year = 1, current_year + 1
    else:
        next_month, next_year = current_month + 1, current_year

    eventos = Evento.objects.filter(
        data_inicio__year=current_year,
        data_inicio__month=current_month
    )

    event_days = set()
    for event in eventos:
        start_day = event.data_inicio.day
        end_day = event.data_fim.day

        for day in range(start_day, end_day + 1):
            event_days.add(day)

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nome_evento = data.get('nome')
            inicio_evento = data.get('inicio')
            fim_evento = data.get('fim')

            inicio_evento = datetime.datetime.strptime(inicio_evento, '%Y-%m-%d').date()
            fim_evento = datetime.datetime.strptime(fim_evento, '%Y-%m-%d').date()

            if inicio_evento > fim_evento:
                return JsonResponse({'success': False, 'message': 'Data de início não pode ser posterior à data de fim.'})

            Evento.objects.create(
                nome=nome_evento,
                data_inicio=inicio_evento,
                data_fim=fim_evento
            )

            return JsonResponse({'success': True})

        except Exception as e:
            print(f"Erro ao processar dados: {str(e)}")
            return JsonResponse({'success': False, 'message': 'Erro ao adicionar evento.'})

    context = {
        'current_year': current_year,
        'current_month': current_month,
        'days': days,
        'empty_days': empty_days,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'today': today.day if current_month == today.month and current_year == today.year else None,
        'event_days': list(event_days),
    }
    return render(request, 'calendario.html', context)

def generate_audio(request):
    if request.method == 'POST':
        text = request.POST.get('text', '')
        
        if text.strip():
            tts = gTTS(text=text, lang='pt', slow=False)
            audio_file = "static/audio/audio_output.mp3"
            tts.save(audio_file)
            
            return JsonResponse({'audio_url': f'/{audio_file}'})
        else:
            return JsonResponse({'error': 'O texto está vazio!'})
    else:
        return JsonResponse({'error': 'Método inválido, use POST'})