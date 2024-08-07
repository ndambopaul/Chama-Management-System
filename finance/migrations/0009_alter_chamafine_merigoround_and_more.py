# Generated by Django 5.0.6 on 2024-07-06 17:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0008_remove_payment_meri_go_round_amount_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chamafine",
            name="merigoround",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="finance.merigoround",
            ),
        ),
        migrations.AlterField(
            model_name="membersaving",
            name="merigoround",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="finance.merigoround",
            ),
        ),
        migrations.AlterField(
            model_name="merigoroundpayment",
            name="merigoround",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="finance.merigoround",
            ),
        ),
        migrations.AlterField(
            model_name="payment",
            name="merigoround",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="finance.merigoround",
            ),
        ),
    ]
