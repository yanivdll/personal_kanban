# Generated by Django 4.1.3 on 2023-02-02 03:01

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("board", "0003_alter_board_owner_delete_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="board",
            name="date_created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="board",
            name="date_modified",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="column",
            name="date_creted",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="column",
            name="date_modified",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="task",
            name="date_created",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="task",
            name="date_modified",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="task",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
    ]
