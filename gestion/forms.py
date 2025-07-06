# gestion/forms.py
from django import forms
from .models import Cliente,Mascota,Consulta
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'direccion', 'telefono']

class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'edad', 'cliente']

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['mascota', 'fecha', 'motivo', 'diagnostico', 'tratamiento', 'observaciones']
        
class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

