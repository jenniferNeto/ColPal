# Generated by Django 4.1.7 on 2023-03-03 06:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pipeline', '0002_alter_historicalpipeline_created_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpipeline',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 3, 1, 38, 37, 380445)),
        ),
        migrations.AlterField(
            model_name='pipeline',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 3, 1, 38, 37, 380445)),
        ),
    ]
