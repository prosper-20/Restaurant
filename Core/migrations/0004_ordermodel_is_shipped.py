# Generated by Django 3.2.9 on 2021-12-03 21:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0003_ordermodel_is_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='is_shipped',
            field=models.BooleanField(default=False),
        ),
    ]
