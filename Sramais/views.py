import datetime
from calendar import monthrange
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.shortcuts import render, get_object_or_404, redirect
from .forms import RamaisForm, UnidadeForm, RegistroForm, FavoritoForm
from .models import Ramais, Unidade, Favorito
from django.contrib import messages
from django.core.paginator import Paginator


def passar_obj_para_base(request):  # Passando os valores do models para o template BASE
    ramais = Ramais.objects.all()
    user = User.objects.all()
    context = {'ramais': ramais, 'user': user}
    return render(request, 'base.html', context)


def pesquisa(request, search):  # Função de pesquisa
    ramais = Ramais.objects.all()
    unidades = Unidade.objects.all()
    pesquisa = Ramais.objects.filter(nome__icontains=search) or Unidade.objects.filter(sigla__icontains=search)

    if pesquisa.exists():  # REDIRECIONANDO PARA PAGINA BUSCA
        return render(request, 'Sramais/busca.html', {'pesquisa': pesquisa, 'ramais': ramais, 'unidades': unidades})

    else:  # REDIRECIONANDO CASO NÃO ACHE O RAMAL
        return render(request, 'Sramais/invalido.html', {'ramais': ramais})


def inicio(request):  # view principal
    hora = datetime.datetime.now()
    dias_do_mes = monthrange(hora.year, hora.month)
    ultimo_dia_do_mes = dias_do_mes[1]
    contador = 0
    i = dias_do_mes[0]
    if hora.day == 1 or hora.day > 1:
        while i <= 6:
            i += 1
            contador += 1
    semana = contador
    for i in range(0, 4):
        if hora.day > semana or hora.day > semana + 7:
            semana = semana + 7
    global favorito
    if request.user.is_authenticated:
        favorito = Favorito.objects.all().filter(user=request.user)

    if not request.user.is_authenticated:
        favorito = None
    if semana > ultimo_dia_do_mes:
        c = semana - ultimo_dia_do_mes
        semana = semana - c

    search = request.GET.get('search')
    hora = datetime.datetime.now
    unidade_lista = Ramais.objects.values('unidade__sigla').annotate(Count('id')).order_by(
        'unidade__sigla').filter(id__count__gt=0)  # filtrando unidades repetidas
    ramais = Ramais.objects.all()
    paginator = Paginator(unidade_lista, 2)
    page = request.GET.get('page')
    unidade = paginator.get_page(page)
    unidades = Unidade.objects.all()
    if search:  # PESQUISA DOS RAMAIS
        return pesquisa(request, search)

    return render(request, 'Sramais/inicio.html',
                  {'ramais': ramais, 'hora': hora, 'unidade': unidade, 'favorito': favorito,'unidades': unidades, 'semana': semana})


def guia(request):  # VIEW DE AJUDA
    search = request.GET.get('search')
    ramais = Ramais.objects.all()  # carregando os dados nessa view para carregar as opções de editar usuario e editar perfil
    if search:  # PESQUISA DOS RAMAIS
        return pesquisa(request, search)

    return render(request, 'Sramais/guia.html', {'ramais': ramais})


@permission_required('is_superuser')
def adicionar(request):
    ramais = Ramais.objects.all()
    if request.method == 'POST':  # Adicionando um usuário
        form = RamaisForm(request.POST, request.FILES)  # formulario dos ramais
        if form.is_valid():  # vendo se são validos
            ramais = form.save(commit=False)
            nome_usuario = ramais.nome[0] + str(ramais.dia_de_nascimento) + str(ramais.mes_de_nascimento)
            user = User.objects.create(username=ramais.nome[0], password=123, email="Não Informado")
            user.set_password("12345")
            ramais.user = user
            ramais.save()  # salvando
            if ramais.admin is True:  # Adicionando ADM
                user.is_superuser = True
                user.save()
                messages.info(request, 'Usuario adicionado com sucesso.')
                return redirect('/')  # RETORNANDO PAGINA PRINCIPAL
            else:  # Não colocando ADM
                user.is_superuser = False
                messages.info(request, 'Usuario adicionado com sucesso.')
                user.save()
                return redirect('/')  # RETORNANDO PAGINA PRINCIPAL
    else:  # CASO ELE NÃO CONSIGA ADICIONAR, MANTENHA OS FORMULÁRIOS
        user_form = RegistroForm()
        form = RamaisForm()

    return render(request, 'Sramais/adicionar.html', {'user_form': user_form, 'form': form, 'ramais': ramais})


@login_required()
def editar_perfil(request, id):  # EDITANDO O PERFIL DO USUARIO
    ramais_form = get_object_or_404(Ramais, pk=id)
    unidade_antiga = ramais_form.unidade
    form = RamaisForm(instance=ramais_form)
    search = request.GET.get('search')
    ramais = Ramais.objects.all()
    if request.user.ramais.unidade != unidade_antiga:
        return redirect('/')
    if request.method == 'POST':  # EDITANDO PERFIL
        form = RamaisForm(request.POST, request.FILES, instance=ramais_form)
        if form.is_valid():
            ramais_form = form.save(commit=False)
            ramais_form.save()
            user = ramais_form.user
            if ramais_form.admin is True and request.user.is_superuser:  # Adicionando ADM
                user.is_superuser = True
                user.save()
                if unidade_antiga != ramais_form.unidade: # pra galera não sair trocando de unidade com adm
                    ramais_form.admin = False
                    ramais_form.save()
                    user.is_superuser = False
                    user.save()
                messages.info(request, 'Perfil Editado com sucesso')
                return redirect('/')
            if ramais_form.admin is False or ramais_form.admin is None:  # Retirando ADM
                user.is_superuser = False
                user.save()
                messages.info(request, 'Perfil Editado com sucesso.')
                return redirect('/')
    if search:  # PESQUISA DOS RAMAIS
        ramais = Ramais.objects.all()
        pesquisa = Ramais.objects.filter(nome__icontains=search) or Unidade.objects.filter(sigla__icontains=search)
        if pesquisa.exists():
            return render(request, 'Sramais/busca.html', {'pesquisa': pesquisa, 'ramais': ramais})
        else:
            return render(request, 'Sramais/invalido.html')
    else:
        return render(request, 'Sramais/editar-perfil.html',
                      {'form': form, 'ramais_form': ramais_form, 'ramais': ramais})


@permission_required('is_superuser')
def delete(request, id):  # DELETANDO USUARIO
    user = get_object_or_404(User, pk=id)
    user.delete()
    messages.info(request, 'Usuário deletado com sucesso.')
    return redirect("Sramais-inicio")


@permission_required('is_superuser')
def unidade(request):  # CRIAR UNIDADE
    search = request.GET.get('search')
    ramais = Ramais.objects.all()
    if request.method == 'POST':
        form = UnidadeForm(request.POST)  # formulario de unidade
        if form.is_valid():
            unidades = form.save(commit=False)
            unidades.save()  # salvando
            messages.info(request, 'Unidade adicionada com sucesso.')
            return redirect('/')
    else:
        form = UnidadeForm()
    if search:  # PESQUISA DOS RAMAIS
        return pesquisa(request, search)

    return render(request, 'Sramais/cadastro_unidades.html', {'form': form, 'ramais': ramais})


def apresentacao(request, nome):  # VIEW SOBRE APRESENTAÇÃO DAS UNIDADES
    ramais = Ramais.objects.all()
    unidades = Unidade.objects.all()
    unidade = Ramais.objects.values('unidade__sigla', 'unidade__nome_completo', 'unidade__descrição').annotate(
        Count('id')).order_by('unidade__sigla').filter(id__count__gt=0)  # não lembro do porque disso
    search = request.GET.get('search')
    if search:  # PESQUISA DOS RAMAIS
        return pesquisa(request, search)
    return render(request, 'Sramais/unidade.html',
                  {'nome': nome, 'ramais': ramais, 'unidade': unidade, 'unidades': unidades})


def registro(request):  # VIEW DE REGISTRO PRINCIPAL
    if request.method == 'POST':
        user_form = RegistroForm(request.POST)
        form = RamaisForm(request.POST, request.FILES)
        if user_form.is_valid() and form.is_valid():
            user = user_form.save()
            ramais = form.save(commit=False)
            ramais.user = user
            ramais.save()
            messages.info(request, 'Usuário Registrado com sucesso.')
            return redirect('/')
    else:
        if request.user.is_authenticated:  # EVITAR QUE PESSOAS LOGADAS ACESSEM A PÁGINA DE REGISTRO
            return redirect('/')
        user_form = RegistroForm()
        form = RamaisForm()
    search = request.GET.get('search')
    if search:  # PESQUISA DOS RAMAIS
        return pesquisa(request, search)
    return render(request, 'Sramais/registro.html', {'user_form': user_form, 'form': form})


@login_required()  # view editar usuario
def editar_usuario(request, id):
    user = get_object_or_404(User, pk=id)
    form = RegistroForm(instance=user)
    search = request.GET.get('search')
    ramais = Ramais.objects.all()
    if search:  # PESQUISA DOS RAMAIS
        pesquisa = Ramais.objects.filter(nome__icontains=search) or Unidade.objects.filter(sigla__icontains=search)
        if pesquisa.exists():
            return render(request, 'Sramais/busca.html', {'pesquisa': pesquisa, 'ramais': ramais})
        else:
            return render(request, 'Sramais/invalido.html')
    if request.user and request.user.username != user.username:
        return redirect('/')
    if request.method == 'POST':
        form = RegistroForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.info(request, 'Usuário Editado com sucesso.')
            return redirect('/')
        else:
            return render(request, 'Sramais/editar-usuario.html', {'form': form, 'user': user})
    else:
        return render(request, 'Sramais/editar-usuario.html', {'form': form, 'user': user, 'ramais': ramais})


@permission_required('is_superuser')  # VIEW QUE EDITA A UNIDADE
def editar_unidade(request, id):
    unidade = get_object_or_404(Unidade, pk=id)
    unidade_antiga = unidade.sigla
    form = UnidadeForm(instance=unidade)
    search = request.GET.get('search')
    if search:  # PESQUISA DOS RAMAIS
        return pesquisa(request, search)
    if request.user.ramais.unidade.sigla != unidade_antiga:
        return redirect('/')
    if request.method == 'POST':
        form = UnidadeForm(request.POST, request.FILES, instance=unidade)
        if form.is_valid():
            unidade = form.save(commit=False)
            unidade.save()
            messages.info(request, 'Unidade Editada com sucesso.')

            return redirect('/')
        else:
            return render(request, 'Sramais/editar-unidade.html', {'form': form, 'unidade': unidade})
    else:
        return render(request, 'Sramais/editar-unidade.html', {'form': form, 'unidade': unidade})


def deletar_unidade(request, id):
    unidade = get_object_or_404(Unidade, pk=id)
    unidade.delete()
    messages.info(request, 'Unidade deletada com sucesso.')
    return redirect("Sramais-inicio")


def criar_perfil(request):
    search = request.GET.get('search')
    if request.method == 'POST':
        form = RamaisForm(request.POST, request.FILES)
        if form.is_valid():
            ramais = form.save(commit=False)
            ramais.user = request.user
            ramais.save()
            messages.info(request, 'Usuário Registrado com sucesso.')
            return redirect('/')
    else:
        form = RamaisForm()
    if search:  # PESQUISA DOS RAMAIS
        return pesquisa(request, search)
    return render(request, 'Sramais/criar-perfil.html', {'form': form})


def adicionar_favoritos(request):
    if request.method == 'POST':
        form = FavoritoForm(request.POST, request.FILES)
        if form.is_valid():
            favoritos = form.save(commit=False)
            favoritos.user = request.user
            favoritos.save()
            messages.info(request, 'Favorito adicionado com sucesso')
            return redirect('/')
    else:
        form = FavoritoForm()
    return render(request, 'Sramais/adicionar-favoritos.html', {'form': form})


def deletar_favorito(request, id):
    favorito = get_object_or_404(Favorito, pk=id)
    favorito.delete()
    messages.info(request, 'Favorito deletado com sucesso')
    return redirect('/')
