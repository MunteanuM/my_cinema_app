# Generated by Django 4.0.6 on 2022-08-03 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basepage', '0008_alter_movie_imdb_rating_alter_movie_meta_score_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='certificate',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='movie',
            name='release_year',
            field=models.CharField(max_length=10),
        ),
    ]
