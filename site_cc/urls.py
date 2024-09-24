from django.urls import path
from . import views


urlpatterns = [
    path('', views.pagina_principal, name='pagina_principal'),
    path('tempo/', views.tempo, name='tempo'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('introducao/', views.introducao, name='introducao'),
    path('equipe/', views.equipe, name='equipe'),
    path('contato/', views.contato, name='contato'),
]
