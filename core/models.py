from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta

# Create your models here.

class Evento(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    data_evento = models.DateTimeField()
    data_criacao = models.DateTimeField(auto_now=True)
    usuarios = models.ForeignKey(User, on_delete=models.CASCADE)
    local = models.CharField(blank=True, null=True, max_length=100)



    class Meta:
        db_table = 'evento'
    
    def __str__(self):
        return self.titulo

    def get_data_evento(self):
        return self.data_evento.strftime('%d/%m/%Y %H:%M')

    def get_local_evento(self):
        return self.local

    def get_data_input_evento(self):
        return self.data_evento.strftime('%Y-%m-%dT%H:%M')
    
    def get_evento_atrasado(self):
        if self.data_evento < datetime.now():
            return True
        else:
            return False

    def get_evento_acaminho(self):
        if self.data_evento < datetime.now() + timedelta(hours=2):
            return True
        else:
            return False

