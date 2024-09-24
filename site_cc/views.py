from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.db.models import Q
import requests
from datetime import datetime, timedelta

def pagina_principal(request):
    return render(request, 'pagina_principal.html', {})

def introducao(request):
    return render(request, 'introducao.html')

def equipe(request):
    return render(request, 'equipe.html')

def contato(request):
    return render(request, 'contato.html')

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
                data_formatada = item['date']
                dia = item['day']

                previsao.append({
                    'data': data_formatada,
                    'descricao': dia['condition']['text'],
                    'temperatura_max': dia['maxtemp_c'],
                    'temperatura_min': dia['mintemp_c'],
                    'umidade': dia['avghumidity'],
                    'precipitacao': dia['totalprecip_mm'],
                    'vento_velocidade': dia['maxwind_kph'],
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