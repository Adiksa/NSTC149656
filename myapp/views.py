import myapp.apps
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Silnik, ModelSamochodu, Samochod
from .forms import SilnikForm, ModelSamochoduForm, SamochodForm
from django.apps import apps


@login_required(login_url='login')
def home(request):
    liczba_silnikow = Silnik.objects.count()
    liczba_modeli_samochodow = ModelSamochodu.objects.count()
    liczba_samochodow = Samochod.objects.count()

    if request.method == 'POST':
        logout(request)
        request.session.flush()  # Wyczyszczenie sesji
        return redirect('logout.html')
    else:
        return render(request, 'home.html', {
            'liczba_silnikow': liczba_silnikow,
            'liczba_modeli_samochodow': liczba_modeli_samochodow,
            'liczba_samochodow': liczba_samochodow,
        })


@login_required(login_url='login')
def car_data(request):
    silniki = Silnik.objects.all()
    modele = ModelSamochodu.objects.all()
    samochody = Samochod.objects.all()

    return render(request, 'car_data.html', {
        'silniki': silniki,
        'modele': modele,
        'samochody': samochody,
    })


def logout_view(request):
        logout(request)
        request.session.flush()
        return render(request, 'logout.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Przekierowanie po zalogowaniu
        else:
            message = 'Nieprawidłowa nazwa użytkownika lub hasło.'
            return render(request, 'login.html', {'message': message})
    else:
        return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def dodaj_silnik(request):
    if request.method == 'POST':
        form = SilnikForm(request.POST)
        if form.is_valid():
            oznaczenie = form.cleaned_data['oznaczenie']
            pojemnosc = form.cleaned_data['pojemnosc']
            moc = form.cleaned_data['moc']
            waga = form.cleaned_data['waga']

            silnik = Silnik(oznaczenie=oznaczenie, pojemnosc=pojemnosc, moc=moc, waga=waga)
            silnik.save()

            messages.success(request, 'Dane zostały dodane do bazy.')
            form = SilnikForm()  # Wyczyszczenie formularza
        else:
            messages.error(request, 'Błedne dane.')

    else:
        form = SilnikForm()

    context = {'form': form}
    return render(request, 'dodaj_silnik.html', context)


def dodaj_model_samochodu(request):
    if request.method == 'POST':
        form = ModelSamochoduForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Dane zostały dodane do bazy.')
            form = ModelSamochoduForm()  # Wyczyszczenie formularza
        else:
            messages.error(request, 'Błedne dane.')
    else:
        form = ModelSamochoduForm()

    context = {'form': form}
    return render(request, 'dodaj_model_samochodu.html', context)


def dodaj_samochod(request):
    if request.method == 'POST':
        form = SamochodForm(request.POST)
        if form.is_valid():
            samochod = form.save(commit=False)
            samochod.user = request.user
            samochod.save()
            messages.success(request, 'Dane zostały dodane do bazy.')
            form = SamochodForm()  # Czyszczenie formularza
        else:
            messages.error(request, 'Błędne dane.')
    else:
        form = SamochodForm()

    context = {'form': form}
    return render(request, 'dodaj_samochod.html', context)


def index(request):
    selected_model = request.POST.get('model', 'silnik')

    silniki = Silnik.objects.all()
    modele_samochodow = ModelSamochodu.objects.all()
    samochody = Samochod.objects.all()
    form = None

    if selected_model == 'silnik':
        form = SilnikForm()
    elif selected_model == 'model_samochodu':
        form = ModelSamochoduForm()
    elif selected_model == 'samochod':
        form = SamochodForm()

    if request.method == 'POST':
        if selected_model == 'silnik':
            form = SilnikForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('index')
        elif selected_model == 'model_samochodu':
            form = ModelSamochoduForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('index')
        elif selected_model == 'samochod':
            form = SamochodForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('index')

    return render(request, 'index.html', {
        'selected_model': selected_model,
        'silniki': silniki,
        'modele_samochodow': modele_samochodow,
        'samochody': samochody,
        'form': form
    })

def edit(request, model, pk):
    if model == 'silnik':
        instance = get_object_or_404(Silnik, pk=pk)
        if request.method == 'POST':
            form = SilnikForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('index')
        else:
            form = SilnikForm(instance=instance)

    elif model == 'model_samochodu':
        instance = get_object_or_404(ModelSamochodu, pk=pk)
        if request.method == 'POST':
            form = ModelSamochoduForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('index')
        else:
            form = ModelSamochoduForm(instance=instance)

    elif model == 'samochod':
        instance = get_object_or_404(Samochod, pk=pk)
        if request.method == 'POST':
            form = SamochodForm(request.POST, instance=instance)
            if form.is_valid():
                form.save()
                return redirect('index')
        else:
            form = SamochodForm(instance=instance)

    return render(request, 'edit.html', {
        'model': model,
        'form': form
    })

def delete(request, model, pk):
    if model == 'silnik':
        obj = get_object_or_404(Silnik, pk=pk)
    elif model == 'model_samochodu':
        obj = get_object_or_404(ModelSamochodu, pk=pk)
    elif model == 'samochod':
        obj = get_object_or_404(Samochod, pk=pk)

    if request.method == 'POST':
        obj.delete()
        return redirect('index')

    return render(request, 'delete.html', {
        'model': model,
        'obj': obj
    })

def show_data(request):
    selected_model = request.GET.get('model', 'Silnik')
    sort_field = request.GET.get('sort_by', 'oznaczenie')
    sort_order = request.GET.get('sort_order', 'asc')
    limit = int(request.GET.get('limit', 5))
    page = int(request.GET.get('page', 1))

    # Pobranie danych dla każdego modelu
    Silniki = Silnik.objects.all()
    ModeleSamochodow = ModelSamochodu.objects.all()
    Samochody = Samochod.objects.all()

    # Sortowanie danych
    if(selected_model == 'Silnik'):
        if sort_order == 'asc':
            Silniki = Silniki.order_by(sort_field)
        else:
            Silniki = Silniki.order_by(f'-{sort_field}')
    if(selected_model == 'ModelSamochodu'):
        if sort_order == 'asc':
            ModeleSamochodow = ModeleSamochodow.order_by(sort_field)
        else:
            ModeleSamochodow = ModeleSamochodow.order_by(f'-{sort_field}')
    if(selected_model == 'Samochod'):
        if sort_order == 'asc':
            Samochody = Samochody.order_by(sort_field)
        else:
            Samochody = Samochody.order_by(f'-{sort_field}')


    # Paginacja danych
    start_index = (page - 1) * limit
    end_index = start_index + limit
    Silniki = Silniki[start_index:end_index]
    ModeleSamochodow = ModeleSamochodow[start_index:end_index]
    Samochody = Samochody[start_index:end_index]

    # Utworzenie kontekstu dla szablonu
    context = {
        'selected_model': selected_model,
        'sort_field': sort_field,
        'sort_order': sort_order,
        'limit': limit,
        'queryset': None,  # Placeholder, które zostanie uzupełnione odpowiednim modelem
    }

    # Wybór odpowiedniego modelu i przypisanie queryset
    if selected_model == 'Silnik':
        context['queryset'] = Silniki
    elif selected_model == 'ModelSamochodu':
        context['queryset'] = ModeleSamochodow
    elif selected_model == 'Samochod':
        context['queryset'] = Samochody

    return render(request, 'show_data.html', context)



# Create your views here.
