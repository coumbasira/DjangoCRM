from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record


def home(request):
    records = Record.objects.all()
    # vérifier si vous avez un compte
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #vérifie si vous etes authentifier
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Vous avez été connecté")
            return redirect('home')
        else:
            messages.success(request, "une erreur s'est produite lors de la connexion, veuillez réessayer...")
            return redirect('home')
    else:
        return render(request, 'home.html', {'records':records})
#django logout 

def logout_user(request):
    logout(request)
    messages.success(request, " vous avez été déconnecté... ")
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #s'authentifier et se connecter
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "inscription valider bienvenue!")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})

def customer_record(request, pk):
    if request.user.is_authenticated:
        #recherche des enregistrements
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record':customer_record})
    else:
        messages.success(request, "vous devez être connecté pour voir cette page!")
        return redirect('home')
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, "supprimer avec succès!")
        return redirect('home')
    else:
        messages.success(request, "Vous devez être connecté!")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
           if form.is_valid():
               add_record = form.save()
               messages.success(request, "enregistrement ajouté!")
               return redirect('home')
        return render(request, 'add_record.html', {'form':form})
    
    else:
        messages.success(request, "Vous devez être connecté!")
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "enregistrement modifier!")
            return redirect('home')
        return render(request, 'update_record.html', {'form':form})
    else:
        messages.success(request, "Vous devez être connecté!")
        return redirect('home')
