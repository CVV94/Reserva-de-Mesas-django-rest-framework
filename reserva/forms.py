from .models import Reserva, Mesa
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django import forms

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ('__all__')
        widgets={
            'nombre_persona': forms.TextInput(attrs={'class':'input'}),
            'telefono': forms.NumberInput(attrs={'class':'input', 'validators': [RegexValidator(r'^\d{1,15}$')]}),
            'fecha_reserva': forms.DateInput(attrs={'type':'date', 'class':'input'}, format='%Y-%m-%d'),
            'hora_reserva': forms.TimeInput(attrs={'type':'time','class':'input'}),
            'cantidad_personas': forms.NumberInput(attrs={'class':'input', 'validators': [MinValueValidator(1), MaxValueValidator(15)]}),
            'estado': forms.Select(attrs={'class':'input'}),
            'mesa_asignada': forms.Select(attrs={'class':'input'}),
            'observaciones': forms.Textarea(attrs={'class':'input','placeholder':'Escribe tus observaciones aquí...'}),
        }

class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ('__all__')
        widgets={
            'numero': forms.NumberInput(attrs={'class':'input'}),
            'capacidad_personas': forms.NumberInput(attrs={'class':'input'}),
        }