# Generated by Django 3.1.3 on 2020-11-18 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0019_auto_20201118_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignsub',
            name='assignment_no',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
