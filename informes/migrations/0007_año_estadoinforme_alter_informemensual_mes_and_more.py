# Generated by Django 4.0.6 on 2022-09-22 13:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('informes', '0006_alter_informemensual_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Año',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30, verbose_name='Año')),
            ],
        ),
        migrations.CreateModel(
            name='EstadoInforme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=30, verbose_name='Estado')),
            ],
        ),
        migrations.AlterField(
            model_name='informemensual',
            name='mes',
            field=models.CharField(choices=[('Enero', '1'), ('Febrero', '2'), ('Marzo', '3'), ('Abril', '4'), ('Mayo', '5'), ('Junio', '6'), ('Julio', '7'), ('Agosto', '8'), ('Septiembre', '9'), ('Octubre', '10'), ('Noviembre', '11'), ('Diciembre', '12')], max_length=100, verbose_name='Mes'),
        ),
        migrations.AlterField(
            model_name='informemensual',
            name='año',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='informes.año'),
        ),
        migrations.AlterField(
            model_name='informemensual',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='informes.estadoinforme'),
        ),
        migrations.AlterField(
            model_name='informepublicador',
            name='estado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='informes.estadoinforme'),
        ),
    ]
