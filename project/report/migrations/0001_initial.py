# Generated by Django 3.0.3 on 2020-04-06 12:54

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='KmGrid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geometry', django.contrib.gis.db.models.fields.PolygonField(blank=True, default=None, null=True, srid=4326)),
                ('population', models.IntegerField(default=300)),
            ],
            options={
                'ordering': ('-id',),
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='KmGridScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geometry', django.contrib.gis.db.models.fields.PolygonField(blank=True, default=None, null=True, srid=4326)),
                ('score_1', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('score_2', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('score_3', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('population', models.IntegerField(default=300)),
                ('total_score', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
            ],
            options={
                'ordering': ('-id',),
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('description', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Statuses',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, default=None, null=True, srid=4326)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='report.Status')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
