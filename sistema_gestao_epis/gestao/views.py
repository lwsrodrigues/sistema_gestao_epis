
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from .models import Colaborador

from django.contrib.auth.models import Group

# Verifica se o usuário é administrador
def is_admin(user):
    return user.is_superuser

# Verifica se o usuário é do grupo "UsuariosComuns"
def is_user_common(user):
    return user.groups.filter(name="UsuariosComuns").exists()

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
@user_passes_test(is_admin_or_common)
def emprestimo(request):
    return render(request, 'emprestimo.html')

# Cadastrar EPI (Apenas Admin pode acessar)
@login_required
@user_passes_test(is_admin)
def cadastrar_epi(request):
    return render(request, 'cadastrar_epi.html')

@login_required
@user_passes_test(is_admin)
def controle_epi(request):
    return render(request, 'controle_epi.html')


def cadastro_colaboradores(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        matricula = request.POST['matricula']
        status = request.POST['status']

        # Verifica se a matrícula já existe
        if Colaborador.objects.filter(matricula=matricula).exists():
            messages.error(request, "Matrícula já cadastrada!")
        else:
            Colaborador.objects.create(nome=nome, matricula=matricula, status=status)
            messages.success(request, "Colaborador cadastrado com sucesso!")

    colaboradores = Colaborador.objects.all()
    return render(request, 'cadastro_colaboradores.html', {'colaboradores': colaboradores})

def deletar_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    colaborador.delete()
    messages.success(request, "Colaborador removido com sucesso!")
    return redirect('cadastro_colaboradores')

def atualizar_colaborador(request, id):
    colaborador = get_object_or_404(Colaborador, id=id)
    if request.method == 'POST':
        colaborador.nome = request.POST['nome']
        colaborador.matricula = request.POST['matricula']
        colaborador.status = request.POST['status']
        colaborador.save()
        messages.success(request, "Colaborador atualizado com sucesso!")
        return redirect('cadastro_colaboradores')

    return render(request, 'cadastro_colaboradores.html', {'colaborador': colaborador})