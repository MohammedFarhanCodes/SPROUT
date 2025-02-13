# Generated by Django 5.1.2 on 2024-10-26 06:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0002_investment'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvestmentTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shares', models.DecimalField(decimal_places=5, max_digits=10)),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('invested_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('investment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to='stock.investment')),
            ],
        ),
    ]
