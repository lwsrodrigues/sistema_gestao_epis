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
    path('deletar_colaborador/<int:id>/', views.deletar_colaborador, name='deletar_colaborador'),
    path('atualizar_colaborador/<int:id>/', views.atualizar_colaborador, name='atualizar_colaborador'),


    # Usuário comum
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user-dashboard/emprestimo/', views.emprestimo, name='emprestimo'),
]
