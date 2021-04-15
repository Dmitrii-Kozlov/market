# Generated by Django 3.1.7 on 2021-04-15 12:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sellers', '0001_initial'),
        ('products', '0013_auto_20210330_1402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='managers',
        ),
        migrations.RemoveField(
            model_name='product',
            name='user',
        ),
        migrations.AddField(
            model_name='product',
            name='seller',
            field=models.ForeignKey(default=4, on_delete=django.db.models.deletion.CASCADE, to='sellers.selleraccount'),
            preserve_default=False,
        ),
    ]