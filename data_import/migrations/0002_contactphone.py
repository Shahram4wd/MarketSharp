# Generated by Django 5.1.1 on 2024-10-28 19:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("data_import", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ContactPhone",
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
                ("contact_id", models.UUIDField()),
                (
                    "assistant_phone",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("work_fax", models.CharField(blank=True, max_length=20, null=True)),
                ("cell_phone", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "company_phone",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
                ("home_phone2", models.CharField(blank=True, max_length=20, null=True)),
                ("home_fax", models.CharField(blank=True, max_length=20, null=True)),
                ("pager", models.CharField(blank=True, max_length=20, null=True)),
                ("work_phone2", models.CharField(blank=True, max_length=20, null=True)),
                ("company_fax", models.CharField(blank=True, max_length=20, null=True)),
                ("home_phone", models.CharField(blank=True, max_length=20, null=True)),
                ("work_phone", models.CharField(blank=True, max_length=20, null=True)),
                ("other_phone", models.CharField(blank=True, max_length=20, null=True)),
                ("cell_phone2", models.CharField(blank=True, max_length=20, null=True)),
                (
                    "other_phone2",
                    models.CharField(blank=True, max_length=20, null=True),
                ),
            ],
            options={
                "verbose_name": "Contact Phone",
                "verbose_name_plural": "Contact Phones",
            },
        ),
    ]
