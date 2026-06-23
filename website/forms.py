#website/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Usuarios

# Validador de seguridad (Capa 2: Backend)
alfanumerico_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9_]*$',
    message='Solo se permiten letras, números y guiones bajos (_).'
)

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        validators=[alfanumerico_validator], 
        label='', 
        widget=forms.TextInput(attrs={'placeholder': 'Nombre de usuario', 'pattern': '^[a-zA-Z0-9_]*$'}) # Capa 1: Frontend
    )
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}))
    first_name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nombre'}))
    last_name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Apellido'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        
    def __init__(self,*args, **kwargs) -> None:
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña', 'pattern': '^[a-zA-Z0-9_]*$'})
            self.fields['password1'].validators.append(alfanumerico_validator)
            self.fields['password1'].label = ''
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirmar contraseña', 'pattern': '^[a-zA-Z0-9_]*$'})
            self.fields['password2'].validators.append(alfanumerico_validator)
            self.fields['password2'].label = ''

class AddUsuarioForm(forms.ModelForm):
    nombre = forms.CharField(required=True, widget=forms.widgets.TextInput(attrs={"placeholder":"Nombre","class":"form-control"}), label="")
    correo = forms.CharField(required=True, widget=forms.widgets.EmailInput(attrs={"placeholder":"Correo electrónico","class":"form-control"}), label="")
    contrasena = forms.CharField(
        validators=[alfanumerico_validator], 
        required=True, 
        widget=forms.widgets.PasswordInput(attrs={"placeholder":"Contraseña","class":"form-control", "pattern":"^[a-zA-Z0-9_]*$"}), 
        label=""
    )
    
    class Meta:
        model = Usuarios
        fields = ('nombre', 'correo', 'contrasena')
