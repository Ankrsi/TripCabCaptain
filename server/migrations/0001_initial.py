# Generated by Django 4.0.3 on 2022-04-21 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cabLatLong',
            fields=[
                ('ip', models.CharField(max_length=50)),
                ('carNum', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('carStatus', models.CharField(max_length=10)),
                ('LatLong', models.CharField(max_length=50)),
            ],
        ),
    ]
