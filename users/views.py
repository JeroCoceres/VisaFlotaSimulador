from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.db.models.signals import post_save
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from users.forms import RegisterForm
from django.contrib.auth.decorators import login_required




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