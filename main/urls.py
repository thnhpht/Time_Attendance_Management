from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('home/', views.home, name='home'),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('sign-out/', views.sign_out, name='sign-out'),
    path('user/', views.user, name='user'),
    path('staff/', views.staff, name='staff'),
]