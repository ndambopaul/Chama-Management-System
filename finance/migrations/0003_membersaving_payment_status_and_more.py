# Generated by Django 5.0.3 on 2024-03-17 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("finance", "0002_remove_payment_paid_payment_total_amount_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="membersaving",
            name="payment_status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Paid", "Paid"),
                    ("Defaulted", "Defaulted"),
                ],
                default="Pending",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="merigoroundpayment",
            name="payment_status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Paid", "Paid"),
                    ("Defaulted", "Defaulted"),
                ],
                default="Pending",
                max_length=255,
            ),
        ),
    ]
