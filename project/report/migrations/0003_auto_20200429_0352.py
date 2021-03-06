# Generated by Django 3.0.3 on 2020-04-29 03:52

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('report', '0002_auto_20200406_2347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='kmgrid',
            options={'managed': True, 'ordering': ('-id',)},
        ),
        migrations.AlterField(
            model_name='report',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, default=None, help_text='Location of the report/user Location', null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='report',
            name='status',
            field=models.ForeignKey(help_text='Status of this report', on_delete=django.db.models.deletion.CASCADE, to='report.Status'),
        ),
        migrations.AlterField(
            model_name='report',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, help_text='Timestamp of report creation'),
        ),
        migrations.AlterField(
            model_name='report',
            name='user',
            field=models.ForeignKey(help_text='Owner/user of this report', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='status',
            name='description',
            field=models.TextField(blank=True, default=None, help_text='Brief description of this status', null=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='name',
            field=models.CharField(default='', help_text='Name of this status', max_length=50),
        ),
    ]
