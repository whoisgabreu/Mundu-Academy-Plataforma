from django.contrib import admin
from .models import ResourceCategory, Resource


@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ['nome', 'slug', 'ordem']
    prepopulated_fields = {'slug': ('nome',)}
    ordering = ['ordem']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'autor', 'categoria', 'formato', 'novo', 'em_alta', 'premium', 'visualizacoes']
    list_filter = ['categoria', 'formato', 'novo', 'em_alta', 'premium']
    search_fields = ['titulo', 'descricao', 'autor']
