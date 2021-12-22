# Generated by Django 3.2.9 on 2021-12-22 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0003_item_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('S', 'Shirt'), ('SW', 'Sports Wear'), ('OW', 'OutWear')], max_length=2),
        ),
        migrations.AlterField(
            model_name='item',
            name='label',
            field=models.CharField(choices=[('P', 'Primary'), ('S', 'Secondary'), ('D', 'Danger')], max_length=1),
        ),
    ]
