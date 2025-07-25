from django import forms
from django.contrib.auth.models import User

class RegistroForm(forms.Form):
    nombre = forms.CharField(max_length=100, required=True, label='Nombre', 
                             widget= forms.TextInput(attrs={
                                 'class': 'form-control',
                                 'placeholder': 'Ingrese su nombre'}))
    apellido = forms.CharField(max_length=100, required=True, label='Apellido',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Ingrese su apellido'}))
    email = forms.EmailField(required=True, label='Email',
                              widget=forms.EmailInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'ejemplo@gmail.com'}))
    provincia = forms.CharField(max_length=50, required=True, label='Provincia',
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control',
                                     'placeholder': 'ej: Buenos Aires'}))
    localidad = forms.CharField(max_length=50, required=True, label='Localidad',
                                 widget=forms.TextInput(attrs={
                                     'class': 'form-control',
                                     'placeholder': 'ej: La Plata'}))
    codigo_postal = forms.CharField(max_length=20, required=True, label='Código Postal',
                                     widget=forms.TextInput(attrs={
                                         'class': 'form-control',
                                         'placeholder': 'ej: 1234'}))
    direccion = forms.CharField(max_length=200, required=True, label='Dirección',
                                 widget=forms.TextInput(attrs={
                                    'class': 'form-control',
                                    'placeholder': 'ej: Av. Siempre Viva 742'}))
    telefono = forms.CharField(max_length=20, required=True, label='Teléfono',
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'ej: 11-1234-5678'}))
    password = forms.CharField(label='Contraseña', required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Contraseña',
    }))
    password2 = forms.CharField(label='Confirmar contraseña', required=True, widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Contraseña'
        }
    ))
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')  # Usar cleaned_data, no self.data
    
        if User.objects.filter(username=nombre).exists():
            raise forms.ValidationError('Usuario ya existente')
    
        return nombre

    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Correo ya registrado')
        
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        
        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'La contraseña no coincide')