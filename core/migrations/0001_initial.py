# Generated by Django 4.2 on 2023-05-07 19:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
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
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "username",
                    models.CharField(db_index=True, max_length=255, unique=True),
                ),
                ("name", models.CharField(blank=True, max_length=254, null=True)),
                (
                    "email",
                    models.EmailField(
                        blank=True,
                        db_index=True,
                        max_length=254,
                        null=True,
                        unique=True,
                    ),
                ),
                ("is_staff", models.BooleanField(default=False)),
                ("is_superuser", models.BooleanField(default=False)),
                ("is_active", models.BooleanField(default=True)),
                ("date_joined", models.DateTimeField(auto_now_add=True, null=True)),
                ("last_login", models.DateTimeField(auto_now_add=True, null=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
        migrations.CreateModel(
            name="Candidate",
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
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("nationality", django_countries.fields.CountryField(max_length=2)),
                ("passport_no", models.CharField(max_length=20, unique=True)),
                ("visa_issued", models.BooleanField(default=False)),
                ("medical_issued", models.BooleanField(default=False)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Interview",
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
                ("client_name", models.CharField(max_length=50)),
                ("start_date", models.DateField()),
                ("interviewer_name", models.CharField(max_length=50)),
                ("cv_file_path", models.CharField(blank=True, max_length=100)),
                ("name", models.CharField(blank=True, max_length=100)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "accessible_users",
                    models.ManyToManyField(to=settings.AUTH_USER_MODEL),
                ),
                ("candidates", models.ManyToManyField(to="core.candidate")),
            ],
        ),
        migrations.CreateModel(
            name="UserInterview",
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
                (
                    "access_control",
                    models.CharField(
                        choices=[
                            ("CL", "Client"),
                            ("AG", "Agent"),
                            ("CO", "My_Company"),
                        ],
                        max_length=2,
                    ),
                ),
                (
                    "interview",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="core.interview"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
