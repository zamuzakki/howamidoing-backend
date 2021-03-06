# Generated by Django 3.0.3 on 2020-05-04 07:52

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('report', '0005_auto_20200429_0715'),
    ]

    operations = [
        migrations.CreateModel(
            name='KmGridScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geometry', django.contrib.gis.db.models.fields.PolygonField(blank=True, default=None, help_text='Geometry of this Grid', null=True, srid=4326)),
                ('score_green', models.DecimalField(decimal_places=2, default=0, help_text='The score of user with latest "All is Well" status in this grid', max_digits=7)),
                ('count_green', models.SmallIntegerField(default=0, help_text='The number of user with latest "All is Well" status in this grid')),
                ('score_yellow', models.DecimalField(decimal_places=2, default=0, help_text='The score of user with latest "We need food or supplies" status in this grid', max_digits=7)),
                ('count_yellow', models.SmallIntegerField(default=0, help_text='The number of user with latest "We need food or supplies" status')),
                ('score_red', models.DecimalField(decimal_places=2, default=0, help_text='The score of user with latest "We need medical help" status in this grid', max_digits=7)),
                ('count_red', models.SmallIntegerField(default=0, help_text='The number of user with latest "We need medical help" status in this grid')),
                ('population', models.IntegerField(default=300, help_text='Number of people in this grid')),
                ('total_score', models.DecimalField(decimal_places=2, default=0, help_text='Total score of this grid', max_digits=7)),
            ],
            options={
                'ordering': ('-id',),
                'managed': True,
            },
        ),
    ]
