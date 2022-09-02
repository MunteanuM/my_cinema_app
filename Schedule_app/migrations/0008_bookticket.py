# Generated by Django 4.0.6 on 2022-08-18 06:53

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Schedule_app', '0007_alter_scheduledmovies_movie'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookTicket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seats', models.CharField(blank=True, default='', max_length=200, null=True, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')])),
                ('schedule', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Schedule_app.schedulemoviecinema')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
