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


  path('buscar_colaboradores/', views.buscar_colaboradores, name='buscar_colaboradores'),
    path('buscar_equipamentos/', views.buscar_equipamentos, name='buscar_equipamentos'),
    path('registrar_emprestimo/', views.registrar_emprestimo, name='registrar_emprestimo'),
    
    path('colaboradores/cadastrar/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('colaboradores/editar/', views.editar_colaborador, name='editar_colaborador'),
    path('colaboradores/excluir/<int:id>/', views.excluir_colaborador, name='excluir_colaborador'),
    path('colaboradores/obter/<int:id>/', views.obter_colaborador, name='obter_colaborador'),
    path('colaboradores/listar/', views.listar_colaboradores, name='listar_colaboradores'),
    path('colaboradores/buscar/', views.buscar_colaboradores, name='buscar_colaboradores'),
  
    path('equipamentos/listar/', views.listar_equipamentos, name='listar_equipamentos'),
    path('equipamentos/cadastrar/', views.cadastrar_epi, name='cadastrar_epi'),
    path('equipamentos/editar/', views.editar_equipamento, name='editar_equipamento'),
    path('equipamentos/excluir/<int:id>/', views.excluir_equipamento, name='excluir_equipamento'),
    path('equipamentos/obter/<int:id>/', views.obter_equipamento, name='obter_equipamento'),
    
    path('emprestimos/listar/', views.listar_emprestimos, name='listar_emprestimos'),
    path('emprestimos/registrar/', views.cadastrar_emprestimo, name='cadastrar_emprestimo'),
    path('emprestimos/editar/', views.editar_emprestimo, name='editar_emprestimo'),
    path('emprestimos/devolver/', views.registrar_devolucao, name='registrar_devolucao'),
    path('emprestimos/excluir/<int:id>/', views.excluir_emprestimo, name='excluir_emprestimo'),
    path('emprestimos/obter/<int:emprestimo_id>/', views.obter_emprestimo, name='obter_emprestimo'),
    path('emprestimos/registrar/', views.registrar_emprestimo, name='registrar_emprestimo'),
    path('emprestimos/devolver/<int:emprestimo_id>/', views.registrar_devolucao, name='registrar_devolucao'),
       
 path('equipamentos/obter/<int:id>/', views.obter_equipamento, name='obter_equipamento'),
 path('editar_equipamento/<int:id>/', views.editar_equipamento, name='editar_equipamento'),
 path('equipamentos/excluir/<int:id>/', views.excluir_equipamento, name='excluir_equipamento'),
    path('buscar-equipamentos/', views.buscar_equipamentos, name='buscar_equipamentos'),
      path('criar_emprestimo/', views.cadastrar_emprestimo, name='criar_emprestimo'),

    # Usuário comum
    path('user-dashboard/', views.user_dashboard, name='user_dashboard'),
  
]
