# Generated by Django 5.1.2 on 2024-10-27 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_delete_wallet'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='pay_extra',
            field=models.CharField(choices=[('roundup_balance', 'Roundup Balance'), ('fixed_percentage', 'Fixed Percentage')], default='roundup_balance', max_length=20),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='pay_extra_for',
            field=models.CharField(choices=[('savings', 'Savings'), ('invest', 'Invest')], default='savings', max_length=20),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='percentage',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]