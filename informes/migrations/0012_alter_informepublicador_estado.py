# Generated by Django 4.0.6 on 2022-10-26 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('informes', '0011_ultimoinforme'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informepublicador',
            name='estado',
            field=models.CharField(default='1', max_length=200),
        ),
    ]
