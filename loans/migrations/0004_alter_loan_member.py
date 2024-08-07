# Generated by Django 5.0.6 on 2024-07-06 18:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("loans", "0003_loan_amount_to_repay"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="member",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="memberloans",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
