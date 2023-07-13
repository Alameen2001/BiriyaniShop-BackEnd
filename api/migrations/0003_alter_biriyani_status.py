# Generated by Django 4.2.2 on 2023-07-12 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_biriyani_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biriyani',
            name='status',
            field=models.CharField(choices=[('-in cart-', '-in cart-'), ('-order placed-', '-order placed-'), ('-order cancelled-', '-order cancelled-')], default='in cart', max_length=200),
        ),
    ]