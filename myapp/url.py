from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('car_data/', views.car_data, name='car_data'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dodaj_silnik/', views.dodaj_silnik, name='dodaj_silnik'),
    path('dodaj_model_samochodu', views.dodaj_model_samochodu, name='dodaj_model_samochodu'),
    path('dodaj_samochod', views.dodaj_samochod, name='dodaj_samochod'),
    path('index', views.index, name='index'),
    path('edit/<str:model>/<int:pk>/', views.edit, name='edit'),
    path('delete/<str:model>/<int:pk>/', views.delete, name='delete'),
    path('show_data/', views.show_data, name='show_data'),
]