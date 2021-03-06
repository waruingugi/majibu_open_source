# Generated by Django 3.0.8 on 2020-07-25 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='subscribers',
            options={'verbose_name': 'Subscriber', 'verbose_name_plural': 'Subscribers'},
        ),
        migrations.AlterField(
            model_name='subscribers',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
