# models.py

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Planta(models.Model):
    nome = models.CharField(max_length=100)
    se_da_bem = models.TextField()
    nao_se_da_bem = models.TextField()
    indiferente = models.TextField()

    def __str__(self):
        return self.nome
