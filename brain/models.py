from django.db import models
from django.conf import settings


class BrainNote(models.Model):
    SOURCE_TYPE_CHOICES = [
        ('aula', 'Aula'),
        ('framework', 'Framework'),
        ('summary', 'Summary'),
        ('manual', 'Manual'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='brain_notes'
    )
    title = models.CharField(max_length=300)
    source = models.CharField(max_length=300, blank=True)
    source_type = models.CharField(
        max_length=20, choices=SOURCE_TYPE_CHOICES, default='manual'
    )
    date = models.CharField(max_length=50, blank=True)
    content = models.TextField(blank=True)
    tags = models.JSONField(default=list, blank=True)
    is_public = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.title


class BrainSavedItem(models.Model):
    TYPE_CHOICES = [
        ('framework', 'Framework'),
        ('summary', 'Summary'),
        ('video', 'Video'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='brain_saved_items'
    )
    item_id = models.CharField(max_length=20)
    title = models.CharField(max_length=300)
    item_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    class Meta:
        unique_together = ('user', 'item_id')

    def __str__(self):
        return self.title


class BrainStreak(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='brain_streaks'
    )
    day = models.CharField(max_length=5)
    active = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'day')

    def __str__(self):
        return f'{self.user.username} - {self.day}: {"✅" if self.active else "❌"}'


class BrainFork(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='brain_forks'
    )
    framework_id = models.CharField(max_length=20)
    framework_title = models.CharField(max_length=300)
    framework_slug = models.SlugField()
    my_version_label = models.CharField(max_length=300, blank=True)
    forked_at = models.CharField(max_length=50, blank=True)
    uses_my_version = models.IntegerField(default=0)
    note = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} forkou {self.framework_title}'


class BrainFollower(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='brain_followers'
    )
    follower_handle = models.CharField(max_length=100)
    since = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.follower_handle} segue {self.user.username}'
