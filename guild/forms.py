from django import forms

from guild.models import Community


class CommunityForm(forms.ModelForm):
    class Meta:
        model = Community
        fields = [
            'name',
            'slug',
            'description',
            'description_long',
            'image',
            'banner',
            'main_color',
            'icon',
            'color',
            'rules',
            'moderators',
            'related',
            'nivel',
            'xp_total',
        ]
        labels = {
            'name': 'Nome',
            'description': 'Descrição',
            'description_long': 'Descrição completa',
            'image': 'Imagem',
            'banner': 'Banner',
            'main_color': 'Cor principal',
            'icon': 'Ícone',
            'color': 'Classe de cor',
            'rules': 'Regras',
            'moderators': 'Moderadores',
            'related': 'Relacionadas',
            'nivel': 'Nível',
            'xp_total': 'XP total',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'prof-form-control'
