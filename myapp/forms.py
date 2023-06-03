from django import forms
from django.core.exceptions import ValidationError
from .models import ModelSamochodu, Silnik, Samochod
from datetime import date

def validate_year(value):
    current_year = date.today().year
    if value < 1886 or value > current_year:
        raise ValidationError(f"Rok produkcji musi być pomiędzy 1886 a {current_year}.")

def validate_not_empty(value):
    if not value:
        raise ValidationError("To pole nie może być puste.")

def validate_greater_than_zero(value):
    if value <= 0:
        raise ValidationError("Liczba musi być większa od zera.")

class SilnikForm(forms.ModelForm):
    class Meta:
        model = Silnik
        fields = ['oznaczenie','pojemnosc','moc','waga']
        labels = {
            'oznaczenie' : 'Oznaczenie',
            'pojemnosc' : 'Pojemnosc',
            'moc' : 'Moc',
            'waga' : 'Waga'
        }

    def clean_model(self):
        model = self.cleaned_data['model']
        return model


class ModelSamochoduForm(forms.ModelForm):
    class Meta:
        model = ModelSamochodu
        fields = ['model', 'rodzaj', 'silnik']
        labels = {
            'model': 'Model',
            'rodzaj': 'Rodzaj pojazdu',
            'silnik': 'Silnik'
        }
        widgets = {
            'silnik': forms.CheckboxSelectMultiple
        }

    def clean_model(self):
        model = self.cleaned_data['model']
        return model


class SamochodForm(forms.ModelForm):
    class Meta:
        model = Samochod
        fields = ['model_samochodu', 'silnik', 'tablica_rejestracyjna', 'kolor', 'rok_produkcji']
        labels = {
            'model_samochodu': 'Model samochodu',
            'silnik': 'Silnik',
            'tablica_rejestracyjna': 'Tablica rejestracyjna',
            'kolor': 'Kolor',
            'rok_produkcji': 'Rok produkcji'
        }

    def clean(self):
        cleaned_data = super().clean()
        model_samochodu = cleaned_data.get('model_samochodu')
        if model_samochodu:
            silnik = cleaned_data.get('silnik')
            if silnik and silnik not in model_samochodu.silnik.all():
                self.add_error('silnik', 'Wybrany silnik nie jest przypisany do tego modelu samochodu.')
        return cleaned_data


