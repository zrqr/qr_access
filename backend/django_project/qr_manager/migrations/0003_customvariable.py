# Generated by Django 4.2.5 on 2023-09-26 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("qr_manager", "0002_rename_data_created_qrcode_date_created"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomVariable",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("value", models.CharField(max_length=255)),
            ],
        ),
    ]
