# gestao/forms.py
from django import forms
from .models import Colaborador

class ColaboradorForm(forms.ModelForm):
    class Meta:
        model = Colaborador  # A classe do modelo que será associada ao formulário
        fields = ['nome', 'matricula', 'status']  # Campos que estarão no formulário
