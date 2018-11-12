# Generated by Django 2.0.7 on 2018-10-26 15:44

from django.db import migrations, models
import django.db.models.deletion
import file.models


class Migration(migrations.Migration):

    dependencies = [
        ('board2', '0006_remove_post_upload'),
        ('file', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='comment',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='board2.Comment'),
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to=file.models.get_upload_to),
        ),
    ]