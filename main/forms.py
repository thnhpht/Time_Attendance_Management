from django.forms import ModelForm
from django import forms
from .models import Config
from django.utils.translation import gettext_lazy as _


class ConfigForm(ModelForm):
    class Meta:
        model = Config
        fields = ('location_add', 'wifi')

        widgets = {
            'location_add': forms.TextInput(attrs={'class': 'form-control input mb-5'}),
            'wifi': forms.TextInput(attrs={'class': 'form-control input mb-5'})
        }

        labels = {
            "location_add": _("Địa điểm chấm công bằng GPS"),
            "wifi": _("Tên wifi"),
        }
