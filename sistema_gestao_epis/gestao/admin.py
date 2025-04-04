from django.contrib import admin
from .models import Colaborador
from .models import Equipamento
from .models import Emprestimo
admin.site.register(Equipamento)
admin.site.register(Colaborador)
# Register your models here.


admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('id', 'equipamento', 'colaborador', 'status', 'data_emprestimo', 'data_devolucao_prevista')
    list_filter = ('status', 'equipamento__tipo', 'colaborador__setor')
    search_fields = ('equipamento__nome', 'colaborador__nome')
    raw_id_fields = ('equipamento', 'colaborador')
    date_hierarchy = 'data_emprestimo'