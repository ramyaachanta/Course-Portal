# Generated by Django 3.1.3 on 2020-11-15 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0009_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='feed_id',
            field=models.AutoField(max_length=100, primary_key=True, serialize=False),
        ),
    ]