# Generated by Django 3.1.7 on 2021-03-28 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_auto_20210328_1337'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thumbnail',
            name='user',
        ),
    ]
