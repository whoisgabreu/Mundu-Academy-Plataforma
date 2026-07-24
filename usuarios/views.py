from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from core.utils import render as app_render


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.POST.get('next', '/'))
        error = 'Usuário ou senha incorretos.'

    return render(request, 'login.html', {'request': request, 'error': error})


def logout_view(request):
    logout(request)
    return redirect('login')


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    error = None
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if password != password2:
            error = 'As senhas não coincidem.'
        elif User.objects.filter(username=username).exists():
            error = 'Este nome de usuário já está em uso.'
        elif email and User.objects.filter(email=email).exists():
            error = 'Este e-mail já está cadastrado.'
        else:
            partes = nome.split(' ', 1)
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=partes[0],
                last_name=partes[1] if len(partes) > 1 else '',
            )
            login(request, user)
            return redirect('index')

    return render(request, 'registro.html', {'request': request, 'error': error})


@login_required(login_url='/login')
def alterar_senha_view(request):
    form = PasswordChangeForm(request.user, request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Senha alterada com sucesso.')
            return redirect('/perfil')
        messages.error(request, 'Revise os campos destacados.')
    return app_render(request, 'alterar_senha.html', {'form': form, 'messages_list': list(messages.get_messages(request))})
