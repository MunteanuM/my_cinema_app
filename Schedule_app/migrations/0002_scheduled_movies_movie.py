# Generated by Django 4.0.6 on 2022-08-05 12:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basepage', '0010_alter_movie_certificate_alter_movie_imdb_rating_and_more'),
        ('Schedule_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='scheduled_movies',
            name='movie',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='basepage.movie'),
        ),
    ]