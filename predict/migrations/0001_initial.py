# Generated by Django 3.0.7 on 2020-06-24 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AgentResponseTime',
            fields=[
                ('time_of_day', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('answer_time', models.FloatField(default=100.0)),
            ],
        ),
    ]
