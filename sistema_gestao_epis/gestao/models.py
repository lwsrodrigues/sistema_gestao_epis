from django.db import models

class Colaborador(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    email = models.EmailField(blank=True, null=True)
    setor = models.CharField(max_length=50, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=[('Ativo', 'Ativo'), ('Inativo', 'Inativo')],
        default='Ativo'
    )
    
    def __str__(self):
        return self.nome
    
from django.db import models
from django.utils import timezone

class Equipamento(models.Model):
    TIPO_CHOICES = [
        ('Capacete', 'Capacete de Segurança'),
        ('Luva', 'Luvas de Proteção'),
        ('Bota', 'Botas de Segurança'),
        ('Óculos', 'Óculos de Proteção'),
    ]
    
    STATUS_CHOICES = [
        ('Disponível', 'Disponível'),
        ('Emprestado', 'Emprestado'),
        ('Manutenção', 'Manutenção'),
    ]
    
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES)
    numero_serie = models.CharField(max_length=50, blank=True, null=True)
    data_fabricacao = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Disponível')
    quantidade = models.PositiveIntegerField(default=1)
    observacoes = models.TextField(blank=True, null=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)  # Verifique se este campo existe
    ultima_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'gestao_equipamento'
        
from django.db import models
        

class Emprestimo(models.Model):
    STATUS_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Devolvido', 'Devolvido'),
        ('Atrasado', 'Atrasado'),
    ]
    
    equipamento = models.ForeignKey('Equipamento', on_delete=models.CASCADE)
    colaborador = models.ForeignKey('Colaborador', on_delete=models.CASCADE)
    data_emprestimo = models.DateField()
    data_devolucao_prevista = models.DateField()
    data_devolucao_real = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Ativo')
    danificado = models.BooleanField(default=False)
    observacoes = models.TextField(blank=True)
    
    
    def __str__(self):
        return f"{self.equipamento} - {self.colaborador}"