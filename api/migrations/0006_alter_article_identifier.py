# Generated by Django 5.1.1 on 2024-09-07 15:01

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_comment_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='identifier',
            field=models.CharField(default=uuid.uuid4, max_length=100, unique=True),
        ),
    ]
