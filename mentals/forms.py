from django.forms import ModelForm
from .models import Appointment
from django import forms

class CrearCitas(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['title', 'professional', 'description', 'important']
        widgets={
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ecribe un titulo'}),
            'professional': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Selecciona el profesional'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Descripción de la cita'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input text-center'}),
        }
