# Generated by Django 3.1.7 on 2021-04-01 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('postname', models.CharField(max_length=50)),
                ('mainphoto', models.ImageField(blank=True, null=True, upload_to='')),
                ('company', models.CharField(max_length=100)),
                ('efficacy', models.CharField(max_length=100)),
                ('way', models.CharField(max_length=100)),
                ('precautions', models.CharField(max_length=100)),
            ],
        ),
    ]
