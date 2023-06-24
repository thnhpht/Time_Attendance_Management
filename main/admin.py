from django.contrib import admin
from .models import User, Check_In, Check_Out, Config

class MyAdminSite(admin.AdminSite):
    site_header = "Administration"

admin_site = MyAdminSite(name="myadmin")
admin.site.register(User)
admin.site.register(Check_In)
admin.site.register(Check_Out)
admin.site.register(Config)




