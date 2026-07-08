from django.db import models
from django.utils.text import slugify


class ResourceCategory(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    ordem = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Categoria de Recurso'
        verbose_name_plural = 'Categorias de Recursos'
        ordering = ['ordem']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome


class Resource(models.Model):
    FORMATOS = [
        ('PDF', 'PDF'),
        ('Planilha', 'Planilha'),
        ('Prompt', 'Prompt'),
        ('Template', 'Template'),
        ('Vídeo', 'Vídeo'),
        ('Tool', 'Ferramenta'),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    url = models.URLField()
    autor = models.CharField(max_length=100)
    thumbnail = models.URLField(blank=True, help_text="URL pública de imagem (Unsplash, etc.)")
    categoria = models.ForeignKey(ResourceCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='recursos')
    formato = models.CharField(max_length=20, choices=FORMATOS, default='PDF')
    novo = models.BooleanField(default=False)
    em_alta = models.BooleanField(default=False)
    premium = models.BooleanField(default=False)
    visualizacoes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Recurso'
        verbose_name_plural = 'Recursos'
        ordering = ['-created_at']

    def __str__(self):
        return self.titulo
