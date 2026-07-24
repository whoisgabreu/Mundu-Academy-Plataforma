from django.contrib import admin
from .models import Curso, Modulo, Aula, ProgressoModulo, Trilha, TrilhaModulo, Desafio, ProgressoDesafio, Certificate, CertificateTemplate, FeaturedContent, Quiz, Questao, Alternativa, TentativaQuiz


class TrilhaModuloInline(admin.TabularInline):
    model = TrilhaModulo
    extra = 1
    fields = ['modulo', 'ordem', 'bloqueado', 'prerequisito']


class AulaInline(admin.TabularInline):
    model = Aula
    extra = 1
    fields = ['titulo', 'video_tipo', 'url_video', 'duracao', 'ordem', 'status', 'is_preview', 'premium']
    ordering = ['ordem']


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'slug', 'ordem', 'status', 'nivel', 'total_aulas', 'duracao_total', 'xp_total', 'tem_certificado']
    list_filter = ['status', 'nivel', 'tem_certificado']
    list_editable = ['ordem', 'status']
    search_fields = ['titulo', 'slug', 'descricao']
    prepopulated_fields = {'slug': ('titulo',)}
    inlines = [AulaInline]


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'modulo', 'video_tipo', 'duracao', 'ordem', 'status', 'is_preview', 'premium']
    list_filter = ['status', 'video_tipo', 'is_preview', 'premium', 'modulo']
    search_fields = ['titulo', 'url_video']


@admin.register(Trilha)
class TrilhaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'area', 'nivel', 'objetivo', 'xp_total', 'tem_certificado']
    list_filter = ['area', 'objetivo', 'tem_certificado']
    search_fields = ['titulo', 'descricao']
    inlines = [TrilhaModuloInline]


@admin.register(Desafio)
class DesafioAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'xp', 'meta', 'icon', 'ativo']
    list_filter = ['tipo', 'ativo']
    search_fields = ['titulo']


@admin.register(ProgressoModulo)
class ProgressoModuloAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'modulo', 'progresso', 'data_inicio']
    list_filter = ['progresso']
    search_fields = ['usuario__username', 'modulo__titulo']


@admin.register(ProgressoDesafio)
class ProgressoDesafioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'desafio', 'progresso', 'data_atualizacao']
    search_fields = ['usuario__username', 'desafio__titulo']


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'modulo', 'trilha', 'template', 'codigo', 'emitido_em']
    list_filter = ['emitido_em']
    search_fields = ['usuario__username', 'codigo']
    readonly_fields = ['codigo', 'emitido_em']


@admin.register(CertificateTemplate)
class CertificateTemplateAdmin(admin.ModelAdmin):
    list_display = ['nome', 'carga_horaria', 'assinatura', 'ativo']
    list_filter = ['ativo']
    list_editable = ['ativo']
    search_fields = ['nome', 'assinatura']


@admin.register(FeaturedContent)
class FeaturedContentAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'ordem', 'ativo', 'participantes']
    list_filter = ['tipo', 'ativo']
    list_editable = ['ordem', 'ativo']


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'instrutor', 'progresso']
    search_fields = ['titulo', 'instrutor']


class AlternativaInline(admin.TabularInline):
    model = Alternativa
    extra = 2
    fields = ['texto', 'correta', 'ordem']


class QuestaoInline(admin.TabularInline):
    model = Questao
    extra = 2
    fields = ['enunciado', 'tipo', 'ordem']
    show_change_link = True


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'modulo', 'aula', 'ordem', 'xp_total', 'aprovacao_percentual', 'max_tentativas', 'status']
    list_filter = ['status', 'modulo', 'aula']
    inlines = [QuestaoInline]


@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    list_display = ['enunciado', 'quiz', 'tipo', 'ordem']
    list_filter = ['tipo', 'quiz']
    inlines = [AlternativaInline]


@admin.register(TentativaQuiz)
class TentativaQuizAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'quiz', 'pontuacao', 'total_questoes', 'aprovado', 'concluido_em']
    list_filter = ['aprovado']
