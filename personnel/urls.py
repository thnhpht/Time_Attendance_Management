from django.urls import path
from . import views

urlpatterns = [
    path('personnel/', views.personnel),
]
