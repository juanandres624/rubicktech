from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages, auth
from django.shortcuts import render, redirect, get_object_or_404


def login(request):

    if request.method == 'POST':
        print("entra antes")
        email = request.POST['email']
        password = request.POST['password']

        print(email + " - " + password)

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Bienvenido ' + user.first_name + " " + user.last_name)
            return redirect('dashboard')
        else:
            messages.error(request, 'Credenciales de usuario invalidas')
            return redirect('login')

    return render(request, 'login.html')

@login_required(login_url = 'login')
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'Ha salido de su cuenta de usuario!')
    return redirect('login')
