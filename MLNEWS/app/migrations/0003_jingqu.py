# Generated by Django 2.2.3 on 2021-11-05 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20210508_2243'),
    ]

    operations = [
        migrations.CreateModel(
            name='JingQu',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('sheng', models.CharField(max_length=32)),
                ('sheng_url', models.CharField(max_length=32)),
                ('city', models.CharField(max_length=32)),
                ('city_url', models.CharField(max_length=32)),
                ('jingqu', models.CharField(max_length=32)),
                ('jingqu_url', models.CharField(max_length=32)),
                ('ever', models.IntegerField()),
                ('never', models.IntegerField()),
                ('level', models.CharField(max_length=32, null=True)),
            ],
            options={
                'verbose_name_plural': '景区表',
            },
        ),
    ]
