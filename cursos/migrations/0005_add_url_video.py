from django.db import migrations
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cursos', '0004_alter_aula_youtube_video_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='aula',
            name='url_video',
            field=embed_video.fields.EmbedVideoField(blank=True, null=True),
        ),
    ]
