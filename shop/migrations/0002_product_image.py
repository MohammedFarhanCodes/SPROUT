# Generated by Django 5.1.2 on 2024-10-19 04:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]