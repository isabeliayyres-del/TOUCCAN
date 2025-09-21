from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from decimal import Decimal

from django.db import models

class Users(models.Model):
    id_usuario = models.AutoField(primary_key=True) 
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    senha = models.CharField(max_length=255)
    data_nascimento = models.DateField(null=True, blank=True)
    foto_perfil = models.CharField(max_length=255, null=True, blank=True)
    telefone = models.CharField(max_length=15, null=True, blank=True)
    ativo = models.BooleanField(default=True)
    ip = models.GenericIPAddressField()
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)
    deletado_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'tbl_usuarios'

    def __str__(self):
        return self.nome
 


