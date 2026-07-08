import re
from django.db import migrations

YOUTUBE_RE = re.compile(r'(?:v=|youtu\.be/|youtube\.com/embed/)([\w-]{11})')


def convert_to_url(video_id):
    if not video_id:
        return None
    # Already a full URL? Don't touch it.
    if video_id.startswith('http://') or video_id.startswith('https://'):
        return video_id
    # Extract ID if it's a partial URL
    match = YOUTUBE_RE.search(video_id)
    if match:
        return f'https://www.youtube.com/watch?v={match.group(1)}'
    # Assume it's already a bare ID
    return f'https://www.youtube.com/watch?v={video_id}'


def forwards(apps, schema_editor):
    Aula = apps.get_model('cursos', 'Aula')
    for aula in Aula.objects.all():
        aula.url_video = convert_to_url(aula.youtube_video_id)
        aula.save(update_fields=['url_video'])


def backwards(apps, schema_editor):
    Aula = apps.get_model('cursos', 'Aula')
    for aula in Aula.objects.all():
        aula.url_video = None
        aula.save(update_fields=['url_video'])


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0005_add_url_video'),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
