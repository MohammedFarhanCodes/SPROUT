# Generated by Django 5.1.2 on 2024-10-27 05:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0004_alter_transaction_transaction_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='SavingsGoal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('priority', models.PositiveIntegerField()),
                ('is_locked', models.BooleanField(default=False)),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='savings_goals', to='wallet.wallet')),
            ],
            options={
                'ordering': ['priority'],
            },
        ),
    ]
