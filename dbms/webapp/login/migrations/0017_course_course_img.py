# Generated by Django 3.1.3 on 2020-11-17 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0016_auto_20201118_0032'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_img',
            field=models.ImageField(default='', upload_to=''),
        ),
    ]
