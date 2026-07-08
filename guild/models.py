from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


class Community(models.Model):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=200)
    members = models.IntegerField(default=0)
    posts_today = models.IntegerField(default=0)
    online_now = models.IntegerField(default=0)
    icon = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    description = models.TextField()
    description_long = models.TextField(blank=True)
    rules = models.JSONField(default=list, blank=True)
    moderators = models.JSONField(default=list, blank=True)
    created_at = models.CharField(max_length=50)
    related = models.JSONField(default=list, blank=True)

    class Meta:
        verbose_name_plural = 'Communities'

    def __str__(self):
        return self.name


class Thread(models.Model):
    POST_TYPE_CHOICES = [
        ('text', 'Text'),
        ('link', 'Link'),
        ('media', 'Media'),
    ]
    community = models.ForeignKey(
        Community, on_delete=models.CASCADE, related_name='threads'
    )
    slug = models.SlugField()
    title = models.CharField(max_length=300)
    author_handle = models.CharField(max_length=100, db_index=True)
    body = models.TextField(blank=True)
    preview = models.TextField(blank=True)
    post_type = models.CharField(
        max_length=20, choices=POST_TYPE_CHOICES, default='text'
    )
    tag = models.CharField(max_length=50, blank=True)
    upvotes = models.IntegerField(default=0)
    replies = models.IntegerField(default=0)
    time_ago = models.CharField(max_length=50)
    url = models.URLField(blank=True, help_text="URL para posts do tipo link")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('community', 'slug')

    def __str__(self):
        return self.title


class Comment(models.Model):
    thread = models.ForeignKey(
        Thread, on_delete=models.CASCADE, related_name='comments'
    )
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='children'
    )
    author_handle = models.CharField(max_length=100, db_index=True)
    body = models.TextField()
    upvotes = models.IntegerField(default=0)
    time_ago = models.CharField(max_length=50)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.author_handle}: {self.body[:50]}'


class Vote(models.Model):
    VALOR_CHOICES = [(1, 'Upvote'), (-1, 'Downvote')]
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    valor = models.SmallIntegerField(choices=VALOR_CHOICES, default=1)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'content_type', 'object_id')
        verbose_name = 'Voto'
        verbose_name_plural = 'Votos'

    def __str__(self):
        return f'{self.usuario.username} → {self.content_type} #{self.object_id}'
