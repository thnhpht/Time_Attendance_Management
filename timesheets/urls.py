from django.urls import path
from . import views

urlpatterns = [
    path('timesheets/', views.timesheets),
]
