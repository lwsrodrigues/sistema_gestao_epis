from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),  
    path('login/', views.login_view, name='login'),  
    
    # Admin Dashboard e subpáginas
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/cadastrar_epi/', views.cadastrar_epi, name='cadastrar_epi'),
    path('admin-dashboard/cadastro_colaboradores/', views.cadastro_colaboradores, name='cadastro_colaboradores'),
    path('admin-dashboard/emprestimo/', views.emprestimo, name='emprestimo'),
    path('admin-dashboard/sair/', views.login_view, name='login'),
    path('admin-dashboard/controle_epi/', views.controle_epi, name='controle_epi'),
    
    
path('cadastro_colaboradores/', views.cadastro_colaboradores, name='cadastro_colaboradores'),
 path('colaboradores/cadastrar/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('colaboradores/editar/', views.editar_colaborador, name='editar_colaborador'),
    path('colaboradores/excluir/<int:id>/', views.excluir_colaborador, name='excluir_colaborador'),
    path('colaboradores/obter/<int:id>/', views.obter_colaborador, name='obter_colaborador'),
  path('colaboradores/listar/', views.listar_colaboradores, name='listar_colaboradores'),


    # Usuário comum
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user-dashboard/emprestimo/', views.emprestimo, name='emprestimo'),
]
