from django.contrib import admin
from .models import Curso, Modulo, Aula, ProgressoModulo, Trilha, TrilhaModulo, Desafio, ProgressoDesafio


class TrilhaModuloInline(admin.TabularInline):
    model = TrilhaModulo
    extra = 1
    fields = ['modulo', 'ordem', 'bloqueado', 'prerequisito']


class AulaInline(admin.TabularInline):
    model = Aula
    extra = 1
    fields = ['titulo', 'youtube_video_id', 'duracao', 'ordem', 'is_preview']
    ordering = ['ordem']


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'nivel', 'total_aulas', 'duracao_total', 'xp_total', 'tem_certificado']
    list_filter = ['nivel', 'tem_certificado']
    search_fields = ['titulo', 'descricao']
    inlines = [AulaInline]


@admin.register(Aula)
class AulaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'modulo', 'youtube_video_id', 'duracao', 'ordem', 'is_preview']
    list_filter = ['is_preview', 'modulo']
    search_fields = ['titulo', 'youtube_video_id']


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


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'instrutor', 'progresso']
    search_fields = ['titulo', 'instrutor']
