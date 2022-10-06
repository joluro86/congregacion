from django.db import models

from admin_congregacion.models import Grupo, Publicador

meses = [('Enero', 'Enero'),('Febrero','Febrero'),('Marzo','Marzo'),('Abril','Abril'),('Mayo','Mayo'),('Junio','Junio'),('Julio','Julio'),('Agosto','Agosto'),('Septiembre','Septiembre'),('Octubre','Octubre'),('Noviembre','Noviembre'),('Diciembre','Diciembre')]

class Año(models.Model):
    nombre= models.CharField('Año', max_length=30)

    class Meta:
        db_table = 'Años'
        managed = True
        verbose_name = "Años"
        verbose_name_plural = "Años"
        ordering= ['id']
    
    def __str__(self):
        return str(self.nombre)

class EstadoInforme(models.Model):
    estado= models.CharField('Estado', max_length=30)
    class Meta:
        db_table = 'estados'
        managed = True
        verbose_name = "Estados Informes Mensuales"
        verbose_name_plural = "Estados Informes Mensuales"
        ordering= ['id']
    
    def __str__(self):
        return str(self.estado)

class InformeMensual(models.Model):
    mes = models.CharField('Mes', choices=meses,max_length=100)
    año = models.ForeignKey(Año, on_delete=models.CASCADE)
    estado = models.ForeignKey(EstadoInforme, on_delete=models.CASCADE)

    class Meta:
        db_table = 'Informe_mensual'
        managed = True
        verbose_name = "Informe Mensual"
        verbose_name_plural = "Informe Mensual"
        ordering= ['-id']
        

    def __str__(self):
        return str(str(self.mes) + " " + str(self.año))
    
class InformePublicador(models.Model):
    informe_mensual = models.ForeignKey(InformeMensual, on_delete=models.CASCADE)
    publicador = models.ForeignKey(Publicador, on_delete=models.CASCADE)
    publicaciones = models.IntegerField(null=True, blank=True)
    videos = models.IntegerField(null=True, blank=True)
    horas = models.IntegerField(default=0)
    revisitas = models.IntegerField(null=True, blank=True)
    cursos = models.IntegerField(null=True, blank=True)
    observaciones = models.CharField(null=True, blank=True, max_length=200)
    estado = models.ForeignKey(EstadoInforme, on_delete=models.CASCADE)    
    
    class Meta:
        verbose_name = "Informe Publicador"
        verbose_name_plural = "Informes Publicador"

    def __str__(self):
        return str(str(self.informe_mensual.mes) + ' - ' + str(self.informe_mensual.año))

class PivoteInformeMensualGrupo(models.Model):
    grupo= models.ForeignKey(Grupo, on_delete=models.CASCADE)
    informe_mensual = models.ForeignKey(InformeMensual, on_delete=models.CASCADE)

    def informes_grupo(grupo):
        return InformePublicador.objects.filter(grupo=grupo)

    def __str__(self):
        return str('Grupo ' + str(self.grupo.numero) + ' - ' + str(self.informe_mensual))

