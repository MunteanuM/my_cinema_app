# Generated by Django 4.1 on 2022-08-26 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basepage', '0019_alter_cinema_city_alter_cinemahall_cinema'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='certificate',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='gross_earnings',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='meta_score',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='star1',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='star2',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='star3',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='star4',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='votes',
        ),
        migrations.AddField(
            model_name='movie',
            name='imdb_id',
            field=models.CharField(default='none', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='imdb_link',
            field=models.URLField(default='none'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='MovieTrailer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imdb_id', models.CharField(max_length=200)),
                ('trailer_id', models.CharField(max_length=100)),
                ('cinema', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='movie', to='basepage.movie')),
            ],
        ),
    ]
