from django.urls import path
from . import views


urlpatterns = [
    path('', views.home),
    path('home/', views.home, name='home'),
    path('sign-in/', views.sign_in, name='sign-in'),
    path('sign-up/', views.sign_up, name='sign-up'),
    path('sign-out/', views.sign_out, name='sign-out'),
    path('staff/', views.staff, name='staff'),
    path('check-in/', views.check_in, name='check-in'),
    path('check-out/', views.check_out, name='check-out'),
    path('timesheets/', views.timesheets, name='timesheets'),
    path('statistic/', views.statistic, name='statistic'),
    path('admin-staff/', views.admin_staff, name='admin-staff'),
    path('admin-timesheets/', views.admin_timesheets, name='admin-timesheets'),
    path('admin-statistic/', views.admin_statistic, name='admin-statistic'),
]