# Generated by Django 2.2.13 on 2021-05-08 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='house',
            name='danjia',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='house',
            name='total',
            field=models.FloatField(),
        ),
    ]