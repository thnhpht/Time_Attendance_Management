from django.urls import path
from . import views

# from .views import UpdateConfigView

urlpatterns = [
    path('', views.home),
    path('home/', views.home, name='home'),
    path('sign-in/', views.signIn, name='sign_in'),
    path('sign-up/', views.signUp, name='sign_up'),
    path('sign-out/', views.signOut, name='sign_out'),
    path('staff/', views.staff, name='staff'),
    path('check-in/', views.checkIn, name='check_in'),
    path('check-out/', views.checkOut, name='check_out'),
    path('timesheets/', views.timesheets, name='timesheets'),
    path('statistic/', views.statistic, name='statistic'),
    path('admin/', views.adminHome),
    path('admin/home/', views.adminHome, name='admin_home'),
    path('admin/staff/', views.manageStaff, name='manage_staff'),
    path('admin/config/', views.config, name='config'),
    path('admin/config-create/', views.createConfig, name='create_config'),
    path('admin/config-update/<int:pk>/', views.updateConfig, name='update_config'),
    path('admin/config-delete/<int:pk>/', views.deleteConfig, name='delete_config'),
]
