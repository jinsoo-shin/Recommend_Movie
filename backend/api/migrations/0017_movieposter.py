# Generated by Django 2.2.4 on 2019-09-23 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_subscribe'),
    ]

    operations = [
        migrations.CreateModel(
            name='MoviePoster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posterUrl', models.CharField(max_length=500)),
            ],
        ),
    ]
