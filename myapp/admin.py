from django.contrib import admin
from .models import ModelSamochodu,Silnik, Samochod
# Register your models here.
admin.site.register(ModelSamochodu)
admin.site.register(Silnik)
admin.site.register(Samochod)