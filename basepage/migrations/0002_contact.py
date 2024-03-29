# Generated by Django 4.0.6 on 2022-07-26 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basepage', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('email', models.CharField(max_length=200, verbose_name='email')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Phone Number')),
                ('city', models.CharField(max_length=200, verbose_name='City')),
                ('subject', models.CharField(max_length=200, verbose_name='Subject')),
                ('message', models.CharField(max_length=200, verbose_name='Message')),
            ],
        ),
    ]
