from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.db.models.signals import post_save
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.forms import RegisterForm
from django.contrib.auth.decorators import login_required








# views.py (users)
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from users.forms import AdminUserEditForm
from costcenter.models import UserProfile
from django.contrib import messages

@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.delete()
        messages.success(request, "Usuario eliminado correctamente.")
        return redirect("admin_edit_users")

    return redirect("admin_edit_users")

@staff_member_required  # Solo permite acceso a administradores
def admin_edit_users(request):
    users = User.objects.filter(is_staff=False, is_superuser=False)
    
    for user in users:
        user.userprofile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == "POST":
        if "redirect_add_users" in request.POST:
            return redirect("/users/register/")
        else:
            for user in users:
                user.username = request.POST.get(f"{user.id}-username", user.username)
                user.userprofile.user_fullname = request.POST.get(f"{user.id}-user_fullname", user.userprofile.user_fullname)
                user.userprofile.unit = request.POST.get(f"{user.id}-unit", user.userprofile.unit)
                
                password = request.POST.get(f"{user.id}-password", None)
                if password:
                    user.set_password(password)

                user.save()  # Guarda cambios en el usuario
                user.userprofile.save()  # Guarda cambios en el perfil del usuario
                
        return redirect("admin_edit_users")  # Redirige para ver los cambios reflejados
    
    return render(request, "users/admin_edit_users.html", {"users": users})

@staff_member_required
def admin_bulk_add_users(request):
    if request.method == "POST":
        num_users = int(request.POST.get("num_users", 1))
        new_users = []
        for i in range(num_users):
            user = User.objects.create(username=f"NuevoUsuario_{i}_{User.objects.count()}")
            UserProfile.objects.create(user=user, user_fullname="", unit="")
            new_users.append(user)
        return redirect("/users/register/details/")
    return render(request, "users/admin_bulk_add_users.html")

@staff_member_required
def admin_complete_user_details(request):
    users = User.objects.filter(username__startswith="NuevoUsuario_")
    for user in users:
        user.userprofile, created = UserProfile.objects.get_or_create(user=user)
    
    if request.method == "POST":
        for user in users:
            user.username = request.POST.get(f"{user.id}-username", user.username)
            user.userprofile.user_fullname = request.POST.get(f"{user.id}-user_fullname", "")
            user.userprofile.unit = request.POST.get(f"{user.id}-unit", "")
            password = request.POST.get(f"{user.id}-password", None)
            if password:
                user.set_password(password)
            user.save()
            user.userprofile.save()
        return redirect("admin_edit_users")
    return render(request, "users/admin_complete_user_details.html", {"users": users})










def login_view(request):
    if request.method == 'GET':
        form = AuthenticationForm()
        context = {"form":form}
        return render(request, 'users/login.html',context=context)
    elif request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
        else:
            context = {
                'errors': form.errors,
            }
            return render(request, 'users/login.html', context)
        

def register(request):
    if request.method == 'GET':
        form = RegisterForm
        context = {"form":form}
        return render(request, 'users/register.html', context=context)
    elif request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        else:
            context = {
                'errors': form.errors,
            }
            return render(request, 'users/register.html', context)
        
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.sessions.models import Session

def logout_view(request):
    logout(request)  # Cierra sesión
    request.session.flush()  # Elimina completamente la sesión del usuario
    Session.objects.all().delete()  # Borra todas las sesiones activas (opcional si quieres limpiar todo)
    return redirect('login')  # Redirige a la página de login
