# Generated by Django 4.2 on 2024-02-27 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_alter_shoppingbasket_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basketitem',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
