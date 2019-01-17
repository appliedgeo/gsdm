# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uploads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shapefile',
            name='shapefile',
            field=models.FileField(upload_to=b'shapefiles'),
        ),
    ]
