# Generated by Django 2.2.3 on 2021-11-06 06:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20211105_2034'),
    ]

    operations = [
        migrations.CreateModel(
            name='JingDian',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('detail', models.CharField(max_length=256)),
                ('img', models.CharField(default='', max_length=256)),
                ('title', models.CharField(max_length=64)),
                ('jingqu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.JingQu', verbose_name='景区的外键')),
            ],
        ),
    ]
