# Generated by Django 4.0.6 on 2022-08-11 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basepage', '0016_remove_city_cinemas_seatmodel_hall_alter_cinema_hall_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cinema',
            old_name='hall',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='cinemahall',
            old_name='seats',
            new_name='cinema',
        ),
    ]
