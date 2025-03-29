from django.db import models

class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    status = models.CharField(
        max_length=10,
        choices=[('Ativo', 'Ativo'), ('Inativo', 'Inativo'), ('Afastado', 'Afastado')]
    )

    def __str__(self):
        return self.nome
