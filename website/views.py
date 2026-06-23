#website/views.py
from .models import Usuarios
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, AddUsuarioForm

# Helper para control de roles
def is_admin(user):
    return user.groups.filter(name='Admin').exists() or user.is_superuser

def home(request):
    records = Usuarios.objects.all()
    return render(request, 'home.html', {'records': records})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In!")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials!")
            return redirect('home')
    return redirect('home')

def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out!")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Registered!")
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form':form})

@login_required(login_url='home')
def customer_record(request, pk):
    customer_record = Usuarios.objects.get(id_usuario=pk)
    return render(request,'record.html',{'customer_record': customer_record})

@login_required(login_url='home')
def delete_record(request, pk):
    if is_admin(request.user):
        delete_it = Usuarios.objects.get(id_usuario=pk)
        delete_it.delete()
        messages.success(request," 📨 ya el registro fue eliminado")
        return redirect('home')
    else:
        messages.error(request," 🚫 Acceso denegado: Se requiere rol de Administrador para eliminar.")
        return redirect('home')

@login_required(login_url='home')
def add_record(request):
    if is_admin(request.user):
        form = AddUsuarioForm(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                messages.success(request, "Se ha agregado el registro correctamente ")
                return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    else:
        messages.error(request," 🚫 Acceso denegado: Se requiere rol de Administrador para agregar.")
        return redirect('home')

@login_required(login_url='home')
def update_record(request, pk):
    if is_admin(request.user):
        current_record = Usuarios.objects.get(id_usuario=pk)
        form = AddUsuarioForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "📝 El registro fue actualizado correctamente")
            return redirect('home')
        return render(request, 'update_record.html', {'form': form})
    else:
        messages.error(request," 🚫 Acceso denegado: Se requiere rol de Administrador para modificar.")
        return redirect('home')
