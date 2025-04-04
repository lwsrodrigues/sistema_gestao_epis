from django.http import JsonResponse  
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login
from .models import Emprestimo, Equipamento, Colaborador  # Adicione esta linha no topo
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.db import transaction  # Adicione esta linha
import json
from django.contrib.auth.models import Group
from django.db.models import Q
from django.db import models
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date
import logging
logger = logging.getLogger(__name__)
from django.views.decorators.http import require_http_methods, require_POST

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



def criar_conta(request):
    return render(request, 'criar_conta.html')

# Página inicial (qualquer um pode acessar)
def home(request):
    return render(request, 'index.html')

def emprestimos_view(request):
    # Busca equipamentos disponíveis (não emprestados)
    equipamentos_disponiveis = Equipamento.objects.filter(
        disponivel=True  # Assumindo que existe um campo 'disponivel' no modelo
    ).order_by('nome')
    
    # Busca todos os colaboradores ativos
    colaboradores = Colaborador.objects.filter(
        ativo=True  # Assumindo que existe um campo 'ativo' no modelo
    ).order_by('nome')
    
    context = {
        'equipamentos_disponiveis': equipamentos_disponiveis,
        'colaboradores': colaboradores,
    }
    
    return render(request, 'emprestimo.html', context)


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
    import pdb; pdb.set_trace()
    try:
        colaborador_id = request.PUT.get('id')
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
    
    
@login_required
@user_passes_test(is_admin)
def cadastrar_epi(request):
    if request.method == 'POST':
        try:
            novo_epi = Equipamento.objects.create(
                nome=request.POST.get('nome'),
                tipo=request.POST.get('tipo'),
                numero_serie=request.POST.get('numero_serie', ''),
                data_fabricacao=request.POST.get('data_fabricacao') or None,
                status=request.POST.get('status', 'Disponível'),
                quantidade=int(request.POST.get('quantidade', 1)),
                observacoes=request.POST.get('observacoes', '')
            )
            return JsonResponse({
                'success': True,
                'message': 'EPI cadastrado com sucesso!',
                'equipamento': {
                    'id': novo_epi.id,
                    'nome': novo_epi.nome,
                    'tipo': novo_epi.tipo,
                    'status': novo_epi.status,
                    'data_cadastro': novo_epi.data_cadastro.strftime('%d/%m/%Y %H:%M') if hasattr(novo_epi, 'data_cadastro') else ''
                }
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    # Para GET ou outros métodos
    return render(request, 'cadastrar_epi.html', {
        'tipos_epi': Equipamento.TIPO_CHOICES,
        'status_choices': Equipamento.STATUS_CHOICES
    })
    
@csrf_exempt
@require_http_methods(['GET'])
@login_required
@user_passes_test(is_admin)
def obter_equipamento(request, id):
    try:
        equipamento = Equipamento.objects.get(id=id)
        return JsonResponse({
            'success': True,
            'id': equipamento.id,
            'nome': equipamento.nome,
            'tipo': equipamento.tipo,
            'numero_serie': equipamento.numero_serie,
            'quantidade': equipamento.quantidade,
            'data_fabricacao': equipamento.data_fabricacao.strftime('%Y-%m-%d') if equipamento.data_fabricacao else None,
            'status': equipamento.status,
            'observacoes': equipamento.observacoes,
            'ultima_atualizacao': equipamento.ultima_atualizacao.strftime('%d/%m/%Y %H:%M')
        })
    except Equipamento.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Equipamento não encontrado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(['PUT'])
@login_required
@user_passes_test(is_admin)
def editar_equipamento(request):
    try:
        data = request.POST
        equipamento_id = data.get('id')
        
        if not equipamento_id:
            return JsonResponse({
                'success': False,
                'message': 'ID do equipamento não fornecido'
            }, status=400)
            
        equipamento = Equipamento.objects.get(id=equipamento_id)
        
        # Atualiza os campos
        equipamento.nome = data.get('nome', equipamento.nome)
        equipamento.tipo = data.get('tipo', equipamento.tipo)
        equipamento.numero_serie = data.get('numero_serie', equipamento.numero_serie)
        equipamento.quantidade = int(data.get('quantidade', equipamento.quantidade))
        equipamento.data_fabricacao = data.get('data_fabricacao', equipamento.data_fabricacao)
        equipamento.status = data.get('status', equipamento.status)
        equipamento.observacoes = data.get('observacoes', equipamento.observacoes)
        
        equipamento.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Equipamento atualizado com sucesso',
            'equipamento': {
                'id': equipamento.id,
                'nome': equipamento.nome,
                'tipo': equipamento.tipo,
                'status': equipamento.status,
                'ultima_atualizacao': equipamento.ultima_atualizacao.strftime('%d/%m/%Y %H:%M')
            }
        })
    except Equipamento.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Equipamento não encontrado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(['DELETE'])
@login_required
@user_passes_test(is_admin)
def excluir_equipamento(request, id):
    try:
        equipamento = Equipamento.objects.get(id=id)
        equipamento.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Equipamento excluído com sucesso'
        })
    except Equipamento.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Equipamento não encontrado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)
        
def listar_equipamentos(request):
    equipamentos = Equipamento.objects.all().values(
        'id', 'nome', 'tipo', 'numero_serie', 'quantidade', 'status'
    )
    return JsonResponse({
        'success': True,
        'equipamentos': list(equipamentos)
    })
    
    
@login_required
@require_POST
def cadastrar_emprestimo(request):
    try:
        data = request.POST
        
        # Campos obrigatórios (sem responsavel_id)
        required_fields = ['equipamento_id', 'colaborador_id', 'data_emprestimo', 'data_devolucao_prevista']
        if not all(data.get(field) for field in required_fields):
            return JsonResponse({
                'success': False, 
                'message': 'Preencha todos os campos obrigatórios'
            }, status=400)  # <<< CORREÇÃO AQUI (status=400)
        
        try:
            equipamento = Equipamento.objects.get(id=data['equipamento_id'])
            if Emprestimo.objects.filter(equipamento=equipamento, status='Ativo').exists():
                return JsonResponse({
                    'success': False, 
                    'message': 'Equipamento já está emprestado'
                }, status=400)  # <<< CORREÇÃO AQUI (status=400)
                
            colaborador = Colaborador.objects.get(id=data['colaborador_id'])
            
        except Equipamento.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'message': 'Equipamento não encontrado'
            }, status=404)  # <<< CORREÇÃO AQUI (status=404)
        except Colaborador.DoesNotExist:
            return JsonResponse({
                'success': False, 
                'message': 'Colaborador não  encontrado'
            }, status=404)  # <<< CORREÇÃO AQUI (status=404)
        
        # Conversão de datas
        try:
            data_emprestimo = datetime.strptime(data['data_emprestimo'], '%Y-%m-%d').date()
            data_devolucao = datetime.strptime(data['data_devolucao_prevista'], '%Y-%m-%d').date()
            
            if data_devolucao <= data_emprestimo:
                return JsonResponse({
                    'success': False, 
                    'message': 'Data de devolução deve ser posterior à data de empréstimo'
                }, status=400)  # <<< CORREÇÃO AQUI (status=400)
                
        except ValueError as e:
            return JsonResponse({
                'success': False, 
                'message': f'Formato de data inválido. Use YYYY-MM-DD. Erro: {str(e)}'
            }, status=400)  # <<< CORREÇÃO AQUI (status=400)
        
        # Criação do empréstimo
        with transaction.atomic():
            emprestimo = Emprestimo.objects.create(
                equipamento=equipamento,
                colaborador=colaborador,
                data_emprestimo=data_emprestimo,
                data_devolucao_prevista=data_devolucao,
                responsavel=request.user,  # Usuário logado como responsável
                observacoes=data.get('observacoes', ''),
                status='Ativo'
            )
            
        return JsonResponse({
            'success': True,
            'message': 'Empréstimo registrado com sucesso!',
            'data': {
                'id': emprestimo.id,
                'equipamento': emprestimo.equipamento.nome,
                'colaborador': emprestimo.colaborador.nome,
                'data_emprestimo': data['data_emprestimo'],
                'data_devolucao_prevista': data['data_devolucao_prevista']
            }
        })
        
    except Exception as e:
        logger.error(f"Erro ao cadastrar empréstimo: {str(e)}", exc_info=True)
        return JsonResponse({
            'success': False, 
            'message': 'Erro interno no servidor'
        }, status=500)  #  <<< CORREÇÃO AQUI (status=500)
        
def listar_emprestimos(request):
    try:
        # Adicionar filtros opcionais
        status_filter = request.GET.get('status')
        colaborador_id = request.GET.get('colaborador_id')
        
        emprestimos = Emprestimo.objects.select_related('equipamento', 'colaborador')
        
        if status_filter:
            emprestimos = emprestimos.filter(status=status_filter)
        if colaborador_id:
            emprestimos = emprestimos.filter(colaborador_id=colaborador_id)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = {
                'emprestimos': [{
                    'id': emp.id,
                    'equipamento': {
                        'id': emp.equipamento.id,
                        'nome': emp.equipamento.nome,
                        'tipo': emp.equipamento.tipo
                    },
                    'colaborador': {
                        'id': emp.colaborador.id,
                        'nome': emp.colaborador.nome,
                        'matricula': emp.colaborador.matricula
                    },
                    'data_emprestimo': emp.data_emprestimo.strftime('%Y-%m-%d'),
                    'data_devolucao_prevista': emp.data_devolucao_prevista.strftime('%Y-%m-%d'),
                    'data_devolucao_real': emp.data_devolucao_real.strftime('%Y-%m-%d') if emp.data_devolucao_real else None,
                    'status': emp.status,
                    'observacoes': emp.observacoes,
                    'dias_atraso': (date.today() - emp.data_devolucao_prevista).days if emp.status == 'Atrasado' else 0
                } for emp in emprestimos]
            }
            return JsonResponse(data)
        
        return render(request, 'emprestimos/listar.html', {'emprestimos': emprestimos})
    
    except Exception as e:
        logger.error(f"Erro ao listar empréstimos: {str(e)}")
        return JsonResponse({'success': False, 'message': 'Erro ao carregar empréstimos'}, status=500)
    
@csrf_exempt
@require_http_methods(["PUT"])
@login_required
@user_passes_test(is_admin)
def editar_emprestimo(request):
    try:
        data = request.POST.dict()
        emprestimo_id = data.get('id')
        
        if not emprestimo_id:
            return JsonResponse({'success': False, 'message': 'ID do empréstimo não fornecido'}, status=400)
        
        emprestimo = Emprestimo.objects.get(id=emprestimo_id)
        
        # Validação de datas
        if 'data_emprestimo' in data and 'data_devolucao_prevista' in data:
            data_emprestimo = datetime.strptime(data['data_emprestimo'], '%Y-%m-%d').date()
            data_devolucao = datetime.strptime(data['data_devolucao_prevista'], '%Y-%m-%d').date()
            
            if data_devolucao < data_emprestimo:
                return JsonResponse({'success': False, 'message': 'Data de devolução não pode ser anterior à data de empréstimo'}, status=400)
        
        # Atualizar equipamento se necessário
        if 'equipamento_id' in data:
            try:
                novo_equipamento = Equipamento.objects.get(id=data['equipamento_id'])
                if novo_equipamento.id != emprestimo.equipamento.id:
                    # Liberar equipamento antigo
                    emprestimo.equipamento.disponivel = True
                    emprestimo.equipamento.save()
                    # Reservar novo equipamento
                    novo_equipamento.disponivel = False
                    novo_equipamento.save()
                    emprestimo.equipamento = novo_equipamento
            except Equipamento.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Novo equipamento não encontrado'}, status=404)
        
        # Atualizar colaborador se necessário
        if 'colaborador_id' in data:
            try:
                colaborador = Colaborador.objects.get(id=data['colaborador_id'])
                emprestimo.colaborador = colaborador
            except Colaborador.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Colaborador não encontrado'}, status=404)
        
        # Atualizar outros campos
        fields_to_update = ['data_emprestimo', 'data_devolucao_prevista', 'status', 'observacoes']
        for field in fields_to_update:
            if field in data:
                setattr(emprestimo, field, data[field])
        
        emprestimo.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Empréstimo atualizado com sucesso',
            'emprestimo': {
                'id': emprestimo.id,
                'equipamento': emprestimo.equipamento.nome,
                'colaborador': emprestimo.colaborador.nome,
                'data_emprestimo': emprestimo.data_emprestimo.strftime('%Y-%m-%d'),
                'data_devolucao_prevista': emprestimo.data_devolucao_prevista.strftime('%Y-%m-%d'),
                'status': emprestimo.status
            }
        })
    
    except Emprestimo.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Empréstimo não encontrado'}, status=404)
    except Exception as e:
        logger.error(f"Erro ao editar empréstimo {emprestimo_id}: {str(e)}")
        return JsonResponse({'success': False, 'message': 'Erro interno no servidor'}, status=500)
        
        
@csrf_exempt
@require_http_methods(["DELETE"])
@login_required
@user_passes_test(is_admin)
def excluir_emprestimo(request, id):
    try:
        emprestimo = Emprestimo.objects.get(id=id)
        
        # Liberar equipamento associado
        equipamento = emprestimo.equipamento
        equipamento.disponivel = True
        equipamento.save()
        
        # Registrar ação antes de deletar
        logger.info(f"Empréstimo {id} excluído por {request.user.username}")
        
        emprestimo.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Empréstimo excluído com sucesso',
            'equipamento_liberado': equipamento.nome
        })
    
    except Emprestimo.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Empréstimo não encontrado'}, status=404)
    except Exception as e:
        logger.error(f"Erro ao excluir empréstimo {id}: {str(e)}")
        return JsonResponse({'success': False, 'message': 'Erro ao excluir empréstimo'}, status=500)
        
@csrf_exempt
@require_http_methods(['GET'])
def obter_emprestimo(request, id):
    try:
        emprestimo = Emprestimo.objects.select_related('equipamento', 'colaborador').get(id=id)
        
        return JsonResponse({
            'success': True,
            'data': {
                'id': emprestimo.id,
                'equipamento': {
                    'id': emprestimo.equipamento.id,
                    'nome': emprestimo.equipamento.nome,
                    'tipo': emprestimo.equipamento.tipo,
                    'disponivel': emprestimo.equipamento.disponivel
                },
                'colaborador': {
                    'id': emprestimo.colaborador.id,
                    'nome': emprestimo.colaborador.nome,
                    'matricula': emprestimo.colaborador.matricula,
                    'setor': emprestimo.colaborador.setor
                },
                'data_emprestimo': emprestimo.data_emprestimo.strftime('%Y-%m-%d'),
                'data_devolucao_prevista': emprestimo.data_devolucao_prevista.strftime('%Y-%m-%d'),
                'data_devolucao_real': emprestimo.data_devolucao_real.strftime('%Y-%m-%d') if emprestimo.data_devolucao_real else None,
                'status': emprestimo.status,
                'observacoes': emprestimo.observacoes,
                'dias_restantes': (emprestimo.data_devolucao_prevista - date.today()).days if emprestimo.status == 'Ativo' else None,
                'dias_atraso': (date.today() - emprestimo.data_devolucao_prevista).days if emprestimo.status == 'Atrasado' else 0
            }
        })
    
    except Emprestimo.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Empréstimo não encontrado'}, status=404)
    except Exception as e:
        logger.error(f"Erro ao obter empréstimo {id}: {str(e)}")
        return JsonResponse({'success': False, 'message': 'Erro ao carregar dados do empréstimo'}, status=500)
        
import json

        
@csrf_exempt
@require_POST
@login_required
def registrar_devolucao(request):
    try:
        emprestimo_id = request.POST.get('emprestimo_id')
        danificado = request.POST.get('danificado') == 'true'
        motivo_dano = request.POST.get('motivo_dano', '')
        
        emprestimo = Emprestimo.objects.get(id=emprestimo_id)
        
        # Atualiza o status
        emprestimo.status = 'Devolvido'
        emprestimo.data_devolucao_real = timezone.now()
        emprestimo.danificado = danificado
        emprestimo.motivo_dano = motivo_dano if danificado else ''
        emprestimo.save()
        
        # Atualiza status do equipamento
        equipamento = emprestimo.equipamento
        equipamento.status = 'Manutenção' if danificado else 'Disponível'
        equipamento.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Devolução registrada com sucesso!'
        })
        
    except Emprestimo.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Empréstimo não encontrado'
        }, status=404)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@login_required
@require_POST
def registrar_emprestimo(request):
    try:
        equipamento_id = request.POST.get('equipamento_id')
        
        # Verifica se o equipamento existe
        try:
            equipamento = Equipamento.objects.get(id=equipamento_id)
        except Equipamento.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Equipamento não encontrado. ID fornecido: ' + str(equipamento_id)
            }, status=404)

        # Restante da lógica...
        emprestimo = Emprestimo.objects.create(
            equipamento=equipamento,  # Usando o objeto diretamente
            colaborador_id=request.POST.get('colaborador_id'),
            data_emprestimo=request.POST.get('data_emprestimo'),
            data_devolucao_prevista=request.POST.get('data_devolucao_prevista'),
            status='Ativo'
        )
        
        return JsonResponse({'success': True, 'message': 'Empréstimo registrado!'})
    
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
@login_required
@require_POST
def registrar_devolucao(request, emprestimo_id):
    try:
        emprestimo = Emprestimo.objects.get(id=emprestimo_id)
        
        # Atualizar dados da devolução
        emprestimo.data_devolucao_real = timezone.now().date()
        emprestimo.status = 'Devolvido'
        emprestimo.danificado = request.POST.get('danificado', 'false') == 'true'
        emprestimo.observacoes = request.POST.get('observacoes', '')
        emprestimo.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Devolução registrada com sucesso!'
        })
        
    except Emprestimo.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Empréstimo não encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)
    
@csrf_exempt
def buscar_colaboradores(request):
    query = request.GET.get('query', '')
    colaboradores = Colaborador.objects.filter(
        models.Q(nome__icontains=query) | 
        models.Q(matricula__icontains=query)
    ).values('id', 'nome', 'matricula')[:10]
    return JsonResponse(list(colaboradores), safe=False)

def buscar_equipamentos(request):
    query = request.GET.get('query', '')  # Termo de busca (ex: "bota")
    filtrar_disponiveis = request.GET.get('disponivel', 'false') == 'true'

    # Filtra equipamentos pelo NOME (ou outro campo existente)
    equipamentos = Equipamento.objects.filter(
        Q(nome__icontains=query) | Q(observacoes__icontains=query)  # Substitua 'observacoes' se necessário
    )

    # Filtra por disponibilidade (se necessário)
    if filtrar_disponiveis:
        ids_indisponiveis = Emprestimo.objects.filter(
            status='Ativo'
        ).values_list('equipamento_id', flat=True)
        equipamentos = equipamentos.exclude(id__in=ids_indisponiveis)

    # Retorna os dados
    dados = list(equipamentos.values('id', 'nome', 'numero_serie', 'status'))
    return JsonResponse(dados, safe=False)

@csrf_exempt
@require_POST
def registrar_emprestimo(request):
    try:
        data = request.POST
        
        # Validação básica
        required_fields = ['equipamento_id', 'colaborador_id', 'data_emprestimo', 'data_devolucao_prevista']
        if not all(data.get(field) for field in required_fields):
            return JsonResponse({
                'success': False,
                'message': 'Todos os campos obrigatórios devem ser preenchidos'
            }, status=400)

        try:
            equipamento = Equipamento.objects.get(id=data['equipamento_id'])
            # Verificação de disponibilidade via empréstimos ativos
            if Emprestimo.objects.filter(equipamento=equipamento, status='Ativo').exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Este equipamento já está emprestado'
                }, status=400)
                
            colaborador = Colaborador.objects.get(id=data['colaborador_id'])
        except Equipamento.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Equipamento não encontrado'
            }, status=404)
        except Colaborador.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Colaborador não encontrado'
            }, status=404)

        # Validação de datas
        try:
            data_emprestimo = datetime.strptime(data['data_emprestimo'], '%Y-%m-%d').date()
            data_devolucao = datetime.strptime(data['data_devolucao_prevista'], '%Y-%m-%d').date()
            
            if data_devolucao <= data_emprestimo:
                return JsonResponse({
                    'success': False,
                    'message': 'Data de devolução deve ser posterior à data de empréstimo'
                }, status=400)
        except ValueError:
            return JsonResponse({
                'success': False,
                'message': 'Formato de data inválido. Use YYYY-MM-DD'
            }, status=400)

        # Cria o empréstimo
        emprestimo = Emprestimo.objects.create(
            equipamento=equipamento,
            colaborador=colaborador,
            data_emprestimo=data['data_emprestimo'],
            data_devolucao_prevista=data['data_devolucao_prevista'],
            observacoes=data.get('observacoes', ''),
            status='Ativo'
        )

        return JsonResponse({
            'success': True,
            'message': 'Empréstimo registrado com sucesso!',
            'emprestimo_id': emprestimo.id
        })

    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Erro ao registrar empréstimo: {str(e)}")
        return JsonResponse({
            'success': False,
            'message': 'Ocorreu um erro interno no servidor'
        }, status=500)
        