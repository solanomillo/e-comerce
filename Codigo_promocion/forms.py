from django import forms

class AplicarCodigoForm(forms.Form):
    codigo = forms.CharField(
        max_length=50,
        label='',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingresa tu código promocional'
        })
    )
