# Generated by Django 3.1.3 on 2020-11-16 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0013_auto_20201116_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='assignment_file',
            field=models.FileField(upload_to='webapp/media/', verbose_name='ENTER FILE:'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='marks',
            field=models.IntegerField(verbose_name='ENTER MARKS:'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='message',
            field=models.CharField(max_length=100, verbose_name='ENTER MESSAGE:'),
        ),
    ]