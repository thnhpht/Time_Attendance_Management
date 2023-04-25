from django.shortcuts import render
from .models import Personnel


# Create your views here.

def personnel(request):
    personnel = Personnel.objects.all()
    return render(request, 'personnel.html', {
        'personnel': personnel,
    })
