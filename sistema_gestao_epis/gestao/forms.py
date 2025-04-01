# gestao/forms.py
from django import forms
from .models import Colaborador, Equipamento

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador  # A classe do modelo que será associada ao formulário
        fields = ['nome', 'matricula', 'status']  # Campos que estarão no formulário

class EquipamentoForm(forms.ModelForm):
    class Meta:
        model = Equipamento
        fields = ['nome', 'tipo', 'numero_serie', 'data_fabricacao', 'status', 'quantidade', 'observacoes']
        widgets = {
            'data_fabricacao': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 2}),
        }
        labels = {
            'nome': 'Nome do Equipamento*',
            'tipo': 'Tipo*',
            'numero_serie': 'Número de Série',
            'data_fabricacao': 'Data de Fabricação',
            'status': 'Status*',
            'quantidade': 'Quantidade*',
            'observacoes': 'Observações'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantidade'].initial = 1
        self.fields['status'].initial = 'Disponível'


                    