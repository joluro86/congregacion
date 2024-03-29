# Generated by Django 4.0.6 on 2022-11-30 15:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin_congregacion', '0004_alter_publicador_options_publicadorirregular'),
        ('informes', '0012_alter_informepublicador_estado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informepublicador',
            name='cursos',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
        migrations.AlterField(
            model_name='informepublicador',
            name='observaciones',
            field=models.CharField(blank=True, default='-', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='informepublicador',
            name='publicaciones',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
        migrations.AlterField(
            model_name='informepublicador',
            name='revisitas',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
        migrations.AlterField(
            model_name='informepublicador',
            name='videos',
            field=models.IntegerField(blank=True, default='0', null=True),
        ),
        migrations.CreateModel(
            name='PivoteUserGrupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_congregacion.grupo')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
