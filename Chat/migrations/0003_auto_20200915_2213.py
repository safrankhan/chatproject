# Generated by Django 2.2.7 on 2020-09-15 16:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Chat', '0002_auto_20200915_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addbot_1',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 9, 15, 22, 13, 31, 758706)),
        ),
    ]
