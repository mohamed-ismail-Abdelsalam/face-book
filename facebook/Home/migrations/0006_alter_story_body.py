# Generated by Django 4.0.6 on 2022-07-26 02:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0005_story'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
    ]