from django import forms
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from django.db.models import Max

from cursos.models import (
    Aula,
    CertificateTemplate,
    Modulo,
    Questao,
    Quiz,
    Alternativa,
    Trilha,
)


CONTROL_CLASS = 'prof-form-control'


class StyledFormMixin:
    def _style_fields(self):
        for field in self.fields.values():
            existing = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = f'{existing} {CONTROL_CLASS}'.strip()


class ModuloForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Modulo
        fields = ['titulo', 'descricao', 'thumbnail', 'ordem', 'status', 'nivel', 'duracao_total', 'xp_total', 'tem_certificado']
        labels = {
            'titulo': 'Nome',
            'descricao': 'Descrição',
            'thumbnail': 'Thumbnail',
            'ordem': 'Ordem',
            'status': 'Status',
            'nivel': 'Nível',
            'duracao_total': 'Duração total',
            'xp_total': 'XP total',
            'tem_certificado': 'Emite certificado',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class AulaForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Aula
        fields = [
            'modulo',
            'titulo',
            'descricao',
            'video_tipo',
            'url_video',
            'video_upload',
            'thumbnail',
            'duracao',
            'tempo_estimado',
            'ordem',
            'material_complementar',
            'status',
            'is_preview',
            'premium',
        ]
        labels = {
            'titulo': 'Nome',
            'descricao': 'Descrição',
            'video_tipo': 'Tipo de vídeo',
            'url_video': 'URL do vídeo',
            'video_upload': 'Upload próprio',
            'thumbnail': 'Thumbnail',
            'duracao': 'Duração',
            'tempo_estimado': 'Tempo estimado',
            'material_complementar': 'Material complementar',
            'status': 'Status',
            'is_preview': 'Gratuita',
            'premium': 'Premium',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()

    def clean(self):
        cleaned = super().clean()
        video_tipo = cleaned.get('video_tipo')
        url_video = cleaned.get('url_video')
        video_upload = cleaned.get('video_upload') or getattr(self.instance, 'video_upload', None)
        if video_tipo == 'upload' and not video_upload:
            self.add_error('video_upload', 'Envie um arquivo de vídeo.')
        if video_tipo in ('youtube', 'vimeo') and not url_video:
            self.add_error('url_video', 'Informe a URL do vídeo.')
        if cleaned.get('is_preview') and cleaned.get('premium'):
            self.add_error('premium', 'Uma aula gratuita não deve ser marcada como premium.')
        return cleaned


class QuizForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Quiz
        fields = [
            'aula',
            'titulo',
            'descricao',
            'ordem',
            'xp_total',
            'aprovacao_percentual',
            'max_tentativas',
            'feedback_automatico',
            'status',
        ]
        labels = {
            'aula': 'Aula',
            'titulo': 'Nome',
            'descricao': 'Descrição',
            'ordem': 'Ordem',
            'xp_total': 'XP total',
            'aprovacao_percentual': 'Nota mínima (%)',
            'max_tentativas': 'Número de tentativas',
            'feedback_automatico': 'Feedback automático',
            'status': 'Status',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ordem'].required = False
        self.fields['ordem'].widget.attrs.setdefault('placeholder', 'Automática')
        self.fields['ordem'].help_text = 'Deixe vazio ou 0 para usar a próxima ordem do módulo.'
        self._style_fields()

    def clean(self):
        cleaned = super().clean()
        aula = cleaned.get('aula')
        if not aula:
            self.add_error('aula', 'Selecione uma aula.')
        max_tentativas = cleaned.get('max_tentativas') or 0
        aprovacao_percentual = cleaned.get('aprovacao_percentual')
        if max_tentativas < 1:
            self.add_error('max_tentativas', 'Informe pelo menos 1 tentativa.')
        if aprovacao_percentual is None or aprovacao_percentual < 0 or aprovacao_percentual > 100:
            self.add_error('aprovacao_percentual', 'Informe uma nota mínima entre 0 e 100.')
        if aula:
            modulo = aula.modulo
            ordem = cleaned.get('ordem') or 0
            if not self.instance.pk and ordem <= 0:
                last_order = Quiz.objects.filter(modulo=modulo).aggregate(max_order=Max('ordem'))['max_order']
                ordem = (last_order or 0) + 1
                cleaned['ordem'] = ordem
            elif ordem < 0:
                self.add_error('ordem', 'A ordem não pode ser negativa.')
            duplicate = Quiz.objects.filter(modulo=modulo, ordem=ordem).exclude(pk=self.instance.pk).exists()
            if duplicate:
                self.add_error('ordem', 'Já existe um quiz nesta ordem para o módulo da aula selecionada.')
        return cleaned

    def save(self, commit=True):
        quiz = super().save(commit=False)
        if quiz.aula_id:
            quiz.modulo = quiz.aula.modulo
        if commit:
            quiz.save()
        return quiz


class QuestaoForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Questao
        fields = ['enunciado', 'tipo', 'ordem']
        labels = {'enunciado': 'Pergunta', 'tipo': 'Tipo', 'ordem': 'Ordem'}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


AlternativaFormSet = inlineformset_factory(
    Questao,
    Alternativa,
    fields=['texto', 'correta', 'ordem'],
    extra=4,
    can_delete=True,
    min_num=2,
    validate_min=True,
)


class CertificateTemplateForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = CertificateTemplate
        fields = ['nome', 'template', 'carga_horaria', 'assinatura', 'logo', 'ativo']
        labels = {
            'nome': 'Nome',
            'template': 'Template',
            'carga_horaria': 'Carga horária',
            'assinatura': 'Assinatura',
            'logo': 'Logo',
            'ativo': 'Ativo',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class CertificateIssueForm(StyledFormMixin, forms.Form):
    usuario = forms.ModelChoiceField(queryset=User.objects.none(), label='Aluno')
    modulo = forms.ModelChoiceField(queryset=Modulo.objects.none(), label='Curso/Módulo', required=False)
    trilha = forms.ModelChoiceField(queryset=Trilha.objects.none(), label='Trilha', required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['usuario'].queryset = User.objects.order_by('first_name', 'username')
        self.fields['modulo'].queryset = Modulo.objects.order_by('ordem', 'titulo')
        self.fields['trilha'].queryset = Trilha.objects.order_by('titulo')
        self._style_fields()

    def clean(self):
        cleaned = super().clean()
        if not cleaned.get('modulo') and not cleaned.get('trilha'):
            raise forms.ValidationError('Selecione um módulo ou uma trilha.')
        return cleaned
