# Generated by Django 4.2.7 on 2025-06-30 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0006_skill_image_alter_skill_icon_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memoryphoto',
            name='image',
            field=models.URLField(help_text='Provide the direct URL to the image.', max_length=500),
        ),
        migrations.AlterField(
            model_name='personalinfo',
            name='profile_photo',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='skill',
            name='image',
            field=models.URLField(blank=True, help_text='(Optional) Use a direct image URL.', max_length=500, null=True),
        ),
    ]
