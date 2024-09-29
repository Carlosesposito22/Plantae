from django.db import models

class Planta(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    se_da_bem = models.TextField(help_text="Plantas que se dão bem com esta planta.")
    nao_se_da_bem = models.TextField(help_text="Plantas que não se dão bem com esta planta.")
    indiferente = models.TextField(help_text="Plantas indiferentes a esta planta.")
    texto_gerado = models.TextField(blank=True, null=True, help_text="Texto gerado pela IA para esta planta.")

    def __str__(self):
        return self.nome
