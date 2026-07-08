from django import forms
from django.contrib.auth.models import User
from usuarios.models import Perfil


class PerfilModelForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label='Nome')
    last_name = forms.CharField(max_length=150, required=False, label='Sobrenome')

    class Meta:
        model = Perfil
        fields = ['cargo', 'empresa', 'localizacao', 'linkedin', 'instagram', 'bio']
        labels = {
            'cargo': 'Cargo / Função',
            'empresa': 'Empresa',
            'localizacao': 'Localização',
            'linkedin': 'LinkedIn',
            'instagram': 'Instagram',
            'bio': 'Sobre você',
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial = user.last_name

    def save(self, commit=True):
        perfil = super().save(commit=False)
        user = perfil.usuario
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            perfil.save()
        return perfil
