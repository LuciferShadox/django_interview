# Generated by Django 4.2 on 2023-05-08 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="candidate",
            name="created_by",
            field=models.CharField(max_length=254),
        ),
    ]
