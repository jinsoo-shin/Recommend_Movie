# Generated by Django 2.2.4 on 2019-09-23 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_auto_20190923_1356'),
    ]

    operations = [
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('imdbId', models.IntegerField()),
                ('posterUrl', models.CharField(max_length=20000)),
            ],
        ),
    ]
