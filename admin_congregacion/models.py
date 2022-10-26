from django.db import models
from admin_congregacion import choices 
from django.contrib.auth.models import User
# Create your models here.

class Congregacion(models.Model):
    numero = models.IntegerField(verbose_name='Número de congregación', unique=True, primary_key=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=100)
    municipio = models.CharField(verbose_name='Municipio o Ciudad', max_length=200)

    def __str__(self):
        return self.nombre + ', ' + self.municipio

    class Meta:
        db_table = 'congregaciones'
        managed = True
        verbose_name = 'Congregacion'
        verbose_name_plural = 'Congregaciones'
        ordering = ['numero']

class Tipo_publicador(models.Model):
    tipo = models.CharField(verbose_name='Tipo publicador', max_length=100)

    class Meta:
        verbose_name = "Tipo de publicador"
        verbose_name_plural = "Tipos de publicador"
        ordering = ['id']

    def __str__(self):
        return self.tipo

class Superintendente(models.Model):
    nombre = models.CharField(verbose_name='Nombre', max_length=200)

    def __str__(self):
        return self.nombre

    class Meta:
        db_table = 'superintendentes'
        managed = True
        verbose_name = 'Superintendente de grupo'
        verbose_name_plural = 'Superintendentes de grupo'
        ordering = ['id']

class Grupo(models.Model):
    numero = models.IntegerField(verbose_name='Número', unique=True, primary_key=True)
    superintendente = models.ForeignKey(Superintendente, on_delete=models.CASCADE)
    congregacion = models.ForeignKey(Congregacion, on_delete=models.CASCADE)
    auxiliar = models.CharField(verbose_name='Auxiliar', null=True, blank=True, max_length=200)

    def __str__(self):
        return 'Grupo ' + str(self.numero) + ' ' + str(self.superintendente)

    class Meta:
        db_table = 'grupos_de_congregacion'
        managed = True
        verbose_name = 'Grupo de congregación'
        verbose_name_plural = 'Grupos de congregación'
        ordering = ['numero']

class PivoteUserToSuperintendente(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    superintendente = models.ForeignKey(Superintendente, on_delete = models.CASCADE)
    grupo = models.ForeignKey(Grupo, on_delete = models.CASCADE)

    class Meta:
        verbose_name = 'Relación Usuario a Super'
        verbose_name_plural = 'Relación Usuario a Super'

    def __str__(self):
       return str(self.user)
        
class EstadoPublicador(models.Model):    
    estado = models.CharField(verbose_name='Estado', max_length=200)

    class Meta:
        verbose_name = "Estado de Publicador"
        verbose_name_plural = "Estados de Publicadores"
        ordering = ['id']

    def __str__(self):
        return self.estado

class Precursorado(models.Model):
    precursorado = models.CharField( verbose_name = 'Precursorado', max_length=100)
    

    class Meta:
        verbose_name = "Precursorado"
        verbose_name_plural = "Precursorado"
        ordering = ['id']

    def __str__(self):
        return self.precursorado
    
class Publicador(models.Model):
    nombre = models.CharField(verbose_name = 'Nombre', max_length=200)
    grupo = models.ForeignKey(Grupo, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Tipo_publicador, on_delete=models.CASCADE)
    sexo = models.CharField(verbose_name='Sexo', choices=choices.sexo, default='----', max_length=50)
    precursor = models.ForeignKey(Precursorado, on_delete=models.CASCADE)
    estado= models.ForeignKey(EstadoPublicador, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Publicador"
        verbose_name_plural = "Publicadores"
        ordering = ['id']

    def __str__(self):
        return self.nombre

class PublicadorInactivo(models.Model):
    
    publicador = models.ForeignKey(Publicador, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Publicadores inactivos"
        verbose_name_plural = "Publicadores inactivos"
        ordering = ['id']

    def __str__(self):
        return str(self.publicador.nombre)


