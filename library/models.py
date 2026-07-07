from django.db import models


class Summary(models.Model):
    summary_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200)
    read_time = models.CharField(max_length=20)
    tag = models.CharField(max_length=100)
    excerpt = models.TextField(blank=True)
    thumbnail = models.URLField(blank=True)
    saves = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Summaries'

    def __str__(self):
        return self.title


class Framework(models.Model):
    COLOR_CHOICES = [
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('accent', 'Accent'),
    ]
    framework_id = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=300)
    description = models.TextField()
    long_description = models.TextField(blank=True)
    format = models.CharField(max_length=100, blank=True)
    uses = models.IntegerField(default=0)
    active_now = models.IntegerField(default=0)
    version = models.CharField(max_length=20, blank=True)
    last_edit_at = models.CharField(max_length=50, blank=True)
    last_editor_handle = models.CharField(max_length=100, blank=True)
    forks = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    reviews_count = models.IntegerField(default=0)
    xp = models.IntegerField(default=0)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES, default='primary')

    def __str__(self):
        return self.title


class FrameworkReview(models.Model):
    framework = models.ForeignKey(
        Framework, on_delete=models.CASCADE, related_name='reviews'
    )
    author_handle = models.CharField(max_length=100)
    rating = models.IntegerField()
    text = models.TextField()
    time_ago = models.CharField(max_length=50)
    helpful = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.author_handle} - {self.rating}/5'
