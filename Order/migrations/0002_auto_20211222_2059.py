# Generated by Django 3.2.9 on 2021-12-22 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.CharField(default='S', max_length=2, verbose_name=(('S', 'Shirt'), ('SW', 'Sports Wear'), ('OW', 'OutWear'))),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='label',
            field=models.CharField(default='P', max_length=1, verbose_name=(('S', 'Shirt'), ('SW', 'Sports Wear'), ('OW', 'OutWear'))),
            preserve_default=False,
        ),
    ]
