# Generated by Django 4.0.6 on 2022-08-08 11:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basepage', '0012_cinemahall_seatmodel_delete_cinema_hall_and_more'),
        ('Schedule_app', '0003_rename_scheduled_movies_scheduledmovies'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleMovieCinema',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cinema', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='basepage.cinema')),
                ('movie', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Schedule_app.scheduledmovies')),
            ],
        ),
    ]
