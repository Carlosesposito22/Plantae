from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView
from django.contrib import messages
from django.http import JsonResponse
import requests
import google.generativeai as genai
from django.shortcuts import render
from datetime import datetime, timedelta
from django.shortcuts import render
from calendar import monthrange
import datetime

# Configure sua API da Google Generative AI
API_KEY = 'AIzaSyC4AVfey0X8ONDz9f_vdw6Sq9yDdhHFowk'
genai.configure(api_key=API_KEY)

# Dicionário de plantas e suas compatibilidades
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
                'previsao': previsao
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
    # Corrigir para usar o método correto de obter a data atual
    today = datetime.date.today()
    current_year = year if year else today.year
    current_month = month if month else today.month

    # Calcular o primeiro e último dia do mês
    first_day_of_month = datetime.date(current_year, current_month, 1)
    _, last_day_of_month = monthrange(current_year, current_month)

    # Calcular o dia da semana do primeiro dia (0=segunda-feira, 6=domingo)
    first_weekday = first_day_of_month.weekday()

    # Gerar lista de dias do mês
    days = list(range(1, last_day_of_month + 1))

    # Calcular os dias vazios (espaços antes do primeiro dia do mês)
    empty_days = [None] * (first_weekday + 1 if first_weekday != 6 else 0)

    # Calcular mês anterior e próximo
    if current_month == 1:
        prev_month = 12
        prev_year = current_year - 1
    else:
        prev_month = current_month - 1
        prev_year = current_year

    if current_month == 12:
        next_month = 1
        next_year = current_year + 1
    else:
        next_month = current_month + 1
        next_year = current_year

    # Renderizar o template
    context = {
        'current_year': current_year,
        'current_month': current_month,
        'days': days,
        'empty_days': empty_days,
        'prev_year': prev_year,
        'prev_month': prev_month,
        'next_year': next_year,
        'next_month': next_month,
        'today': today.day if current_month == today.month and current_year == today.year else None  # Verificar se o mês/ano é o atual
    }

    return render(request, 'calendario.html', context)
