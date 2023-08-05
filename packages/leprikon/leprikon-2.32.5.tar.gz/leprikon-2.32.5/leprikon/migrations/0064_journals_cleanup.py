# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-08-15 15:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("leprikon", "0063_journals"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="journalentry",
            name="subject",
        ),
        migrations.RemoveField(
            model_name="subject",
            name="evaluation",
        ),
        migrations.RemoveField(
            model_name="subject",
            name="plan",
        ),
        migrations.RemoveField(
            model_name="subject",
            name="risks",
        ),
        migrations.AlterField(
            model_name="journalentry",
            name="journal",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="journal_entries",
                to="leprikon.Journal",
                verbose_name="journal",
            ),
        ),
    ]
