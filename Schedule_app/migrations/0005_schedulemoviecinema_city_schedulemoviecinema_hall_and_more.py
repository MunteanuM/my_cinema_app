# Generated by Django 4.0.6 on 2022-08-08 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basepage', '0013_remove_cinema_city_city'),
        ('Schedule_app', '0004_schedulemoviecinema'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedulemoviecinema',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='basepage.city'),
        ),
        migrations.AddField(
            model_name='schedulemoviecinema',
            name='hall',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='basepage.cinemahall'),
        ),
        migrations.AddField(
            model_name='schedulemoviecinema',
            name='playing',
            field=models.DateTimeField(null=True),
        ),
    ]
