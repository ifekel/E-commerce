# Generated by Django 4.1.2 on 2023-01-08 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_orderitem_customer_alter_order_customer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='customer',
        ),
    ]
