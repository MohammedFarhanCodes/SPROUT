# Generated by Django 5.1.2 on 2024-10-21 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='transaction_history',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]