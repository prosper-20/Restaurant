# Generated by Django 3.2.9 on 2021-12-31 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Order', '0002_alter_address_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('S', 'Snacks'), ('E', 'Entre'), ('D', 'Drink'), ('A', 'Appetizer'), ('MC', 'Main Course')], max_length=2),
        ),
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
