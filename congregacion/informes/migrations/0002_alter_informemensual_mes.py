# Generated by Django 3.2.13 on 2022-06-30 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('informes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informemensual',
            name='mes',
            field=models.CharField(choices=[('1', 'Enero'), ('2', 'Febrero'), ('3', 'Marzo'), ('4', 'Abril'), ('5', 'Mayo'), ('6', 'Junio'), ('7', 'Julio'), ('8', 'Agosto'), ('9', 'Septiembre'), ('10', 'Octubre'), ('11', 'Noviembre')], max_length=100, verbose_name='Mes'),
        ),
    ]
