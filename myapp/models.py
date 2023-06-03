from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
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

# Create your models here.


class Silnik(models.Model):
    oznaczenie = models.CharField(max_length=50, validators=[validate_not_empty])
    pojemnosc = models.IntegerField(validators=[validate_not_empty, validate_greater_than_zero])
    moc = models.IntegerField(validators=[validate_not_empty, validate_greater_than_zero])
    waga = models.IntegerField(validators=[validate_not_empty, validate_greater_than_zero])

    objects = models.Manager()

    def __str__(self):
        return self.oznaczenie

    class Meta:
        verbose_name = "Silnik"
        verbose_name_plural = "Silniki"
        ordering = ['oznaczenie']



class ModelSamochodu(models.Model):
    typPojazdu = [
        ("o", "osobowy"),
        ("t", "terenowy"),
        ("s", "sportowy")
    ]
    model = models.CharField(max_length=50)
    rodzaj = models.CharField(max_length=1, choices=typPojazdu)
    silnik = models.ManyToManyField(Silnik)

    objects = models.Manager()

    def __str__(self):
        return self.model

    class Meta:
        verbose_name = "Model samochodu"
        verbose_name_plural = "Modele samochodów"
        ordering = ['model']


class Samochod(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    model_samochodu = models.ForeignKey(ModelSamochodu, on_delete=models.CASCADE, related_name='samochody')
    silnik = models.ForeignKey(Silnik, on_delete=models.CASCADE)
    tablica_rejestracyjna = models.CharField(max_length=50, validators=[validate_not_empty])
    kolor = models.CharField(max_length=50, validators=[validate_not_empty])
    rok_produkcji = models.IntegerField(validators=[validate_year])

    objects = models.Manager()

    def __str__(self):
        return self.tablica_rejestracyjna

    class Meta:
        verbose_name = "Samochód"
        verbose_name_plural = "Samochody"
        ordering = ['tablica_rejestracyjna']
