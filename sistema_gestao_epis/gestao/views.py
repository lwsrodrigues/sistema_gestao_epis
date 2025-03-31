from django.http import JsonResponse  
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from .models import Colaborador
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import Group
from django.db import models
from django.views.decorators.http import require_http_methods

# Verifica se o usuário é administrador
def is_admin(user):
    return user.is_superuser

# Verifica se o usuário é do grupo "UsuariosComuns"
def is_user_common(user):
    return user.groups.filter(name="UsuariosComuns").exists()

def cadastro_colaboradores(request):
    colaboradores = Colaborador.objects.all().order_by('-id')  # Ordena por ID decrescente
    return render(request, 'cadastro_colaboradores.html', {'colaboradores': colaboradores})

# Função para verificar se o usuário tem permissão para acessar a página
def is_admin_or_common(user):
    return is_admin(user) or is_user_common(user)

# Página inicial (qualquer um pode acessar)
def home(request):
    return render(request, 'index.html')



# Login View com Redirecionamento Diferente
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')  # Usa `.get()` para evitar erro caso não exista
        password = request.POST.get('password')  # Usa `.get()` para evitar erro caso não exista

        if username and password:
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # Redireciona com base no tipo de usuário
                if user.is_superuser:
                    return redirect('/admin-dashboard/')  # Página para administradores
                else:
                    return redirect('/user-dashboard/')  # Página para usuários comuns
            else:
                return render(request, 'login.html', {'error': 'Usuário ou senha inválidos'})
        else:
            return render(request, 'login.html', {'error': 'Preencha todos os campos'})

    return render(request, 'login.html')

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'index.html')

@login_required
@user_passes_test(is_admin)
def controle_epi(request):
    return render(request, 'controle_epi.html')

# Painel do Usuário Comum
@login_required
@user_passes_test(is_user_common)
def user_dashboard(request):
    return render(request, 'user_dashboard.html')

# Cadastro de Colaboradores (Apenas Admins podem acessar)
@login_required
@user_passes_test(is_admin)
def cadastro_colaboradores(request):
    return render(request, 'cadastro_colaboradores.html')

# Empréstimos (Usuários Comuns e Admins podem acessar)
@login_required
@user_passes_test(is_admin)
def emprestimo(request):
    return render(request, 'emprestimo.html')

# Cadastrar EPI (Apenas Admin pode acessar)
@login_required
@user_passes_test(is_admin)
def cadastrar_epi(request):
    return render(request, 'cadastrar_epi.html')




 # Apenas para desenvolvimento, remova em produção
@require_http_methods(["POST"])
def cadastrar_colaborador(request):
    try:
        novo_colaborador = Colaborador.objects.create(
            nome=request.POST.get('nome'),
            matricula=request.POST.get('matricula'),
            email=request.POST.get('email'),
            setor=request.POST.get('setor'),
            status=request.POST.get('status'),
            observacoes=request.POST.get('observacoes', '')
        )
        return JsonResponse({
            'success': True,
            'id': novo_colaborador.id,
            'nome': novo_colaborador.nome,
            'matricula': novo_colaborador.matricula,
            'email': novo_colaborador.email,
            'setor': novo_colaborador.setor,
            'status': novo_colaborador.status,
            'observacoes': novo_colaborador.observacoes
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)
@require_http_methods(["PUT"])
def editar_colaborador(request):
    try:
        colaborador_id = request.POST.get('id')
        if not colaborador_id:
            return JsonResponse({'success': False, 'message': 'ID do colaborador não fornecido'}, status=400)
            
        colaborador = Colaborador.objects.get(id=colaborador_id)
        colaborador.id = colaborador_id
        colaborador.nome = request.POST.get('nome')
        colaborador.matricula = request.POST.get('matricula')
        colaborador.email = request.POST.get('email')
        colaborador.setor = request.POST.get('setor')
        colaborador.status = request.POST.get('status')
        colaborador.observacoes = request.POST.get('observacoes', '')
        
        colaborador.save()        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=400)

@require_http_methods(["DELETE"])
def excluir_colaborador(request, id):
    try:
        colaborador = Colaborador.objects.get(id=id)
        colaborador.delete()
        return JsonResponse({'success': True})
    except Colaborador.DoesNotExist:
        return JsonResponse({'success': False}, status=404)

@require_http_methods(["GET"])
def obter_colaborador(request, id):
    try:
        colaborador = Colaborador.objects.get(id=id)
        return JsonResponse({
            'success': True,
            'id': colaborador.id,
            'nome': colaborador.nome,
            'matricula': colaborador.matricula,
            'email': colaborador.email,
            'setor': colaborador.setor,
            'status': colaborador.status,
            'observacoes': colaborador.observacoes
        })
    except Colaborador.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Colaborador não encontrado'}, status=404)
    
    
def listar_colaboradores(request):
    colaboradores = Colaborador.objects.all().values('id', 'nome', 'matricula', 'email', 'setor', 'status')
    return JsonResponse({
        'success': True,
        'colaboradores': list(colaboradores)  # Converte para lista
    })