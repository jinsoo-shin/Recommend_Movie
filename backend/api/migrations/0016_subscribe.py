# Generated by Django 2.2.4 on 2019-09-23 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_algorithmresult'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('expiration', models.CharField(max_length=100)),
            ],
        ),
    ]
