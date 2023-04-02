# Generated by Django 4.1.7 on 2023-04-02 20:06

import accounts.utils
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0024_alter_user_username"),
    ]

    operations = [
        migrations.RenameField(
            model_name="user",
            old_name="created_dt",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="user",
            old_name="updated_dt",
            new_name="updated_at",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="bio",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="birth_date",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="location",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="status",
        ),
        migrations.AddField(
            model_name="profile",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                db_index=True,
                default=accounts.utils.user_6_digit,
                max_length=32,
                unique=True,
            ),
        ),
    ]
