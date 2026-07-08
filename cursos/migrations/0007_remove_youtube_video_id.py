import embed_video.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0006_migrate_youtube_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aula',
            name='youtube_video_id',
        ),
        migrations.AlterField(
            model_name='aula',
            name='url_video',
            field=embed_video.fields.EmbedVideoField(help_text='Cole a URL do YouTube ou Vimeo aqui'),
        ),
    ]
