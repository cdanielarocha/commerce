# Generated by Django 3.0.5 on 2021-04-27 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='photo',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
