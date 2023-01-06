from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib import messages, auth
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import RegistrationForm
from accounts.models import Account
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

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

@login_required(login_url = 'login')
def registerUser(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                               email=email, password=password)
            user.phone_number = phone_number
            user.admin_id = str(request.user)
            user.save()

            return redirect('viewUsers')
    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/newUser.html', context)

@login_required(login_url = 'login')
def viewUsers(request):

    all_users = get_all_users(str(request.user))

    context = {
        'users' : all_users
    }

    return render(request, 'accounts/viewUser.html', context)


@csrf_exempt
def deleteUser(request,username):

    try:
        account = Account.objects.get(username=username)
    except Account.DoesNotExist:
        account = None

    if request.method == "GET":
        username = request.GET.get("username", None)
        user_data = Account.objects.get(username=username)
        user_data.delete()

        return JsonResponse({"message": "success"}, status=200)

    

def get_all_users(adminId):
    
    return Account.objects.filter(is_active=True,is_superadmin=False,admin_id=adminId)
