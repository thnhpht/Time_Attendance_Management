from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('', include('personnel.urls')),
    path('', include('check_in.urls')),
    path('', include('check_out.urls')),
    path('', include('timesheets.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
