from django.urls import path
from . import views

urlpatterns = [
    path('check-in/', views.check_in),
]
