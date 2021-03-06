# Generated by Django 2.0.7 on 2018-10-26 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0002_auto_20181026_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='on_writing',
            field=models.CharField(choices=[('Y', 'Yes'), ('N', 'No')], default='Y', max_length=1),
        ),
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='upload/%Y%m%d/'),
        ),
    ]
