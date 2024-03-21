# Generated by Django 5.0.3 on 2024-03-19 20:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0007_payment_amount_fined_payment_chama_amount_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="payment",
            name="meri_go_round_amount",
        ),
        migrations.AddField(
            model_name="payment",
            name="merigoround",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="finance.merigoround",
            ),
        ),
    ]
