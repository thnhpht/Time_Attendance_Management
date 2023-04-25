from django.urls import path
from . import views

urlpatterns = [
    path('check-out/', views.check_out),
]
