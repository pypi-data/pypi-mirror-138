# Generated by Django 3.2 on 2021-04-22 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instrument', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variable',
            name='value',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
