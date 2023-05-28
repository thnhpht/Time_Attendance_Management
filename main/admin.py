from django.contrib import admin
from .models import User, Check_In, Check_Out


admin.site.register(User)
admin.site.register(Check_In)
admin.site.register(Check_Out)
