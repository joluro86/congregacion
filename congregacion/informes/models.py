from django.db import models

from admin_congregacion.models import Publicador

estado= [('1','Abierto'),('0','Cerrado')]
meses = [('1', 'Enero'),('2','Febrero'),('3','Marzo'),('4','Abril'),('5','Mayo'),('6','Junio'),('7','Julio'),('8','Agosto'),('9','Septiembre'),('10','Octubre'),('11','Noviembre')]
años = [('1', '2022'),('2','2023'),('3','2024'),('5','2025')]

class InformeMensual(models.Model):
    mes = models.CharField('Mes', choices=meses,max_length=100)
    año = models.CharField('Año',choices=años,max_length=100)
    estado = models.CharField('Estado', choices=estado, max_length=100)

    class Meta:
        db_table = 'Informe_mensual'
        managed = True
        verbose_name = "Informe Mensual"
        verbose_name_plural = "Informes Mensuales"
        ordering= ['id']
        

    def __str__(self):
        return 'Mes: ' + str(self.mes) + ' ' + str(self.año)
    
class InformePublicador(models.Model):
    informe_mensual = models.ForeignKey(InformeMensual, on_delete=models.CASCADE)
    publicador = models.ForeignKey(Publicador, on_delete=models.CASCADE)
    publicaciones = models.IntegerField(null=True, blank=True)
    videos = models.IntegerField(null=True, blank=True)
    horas = models.IntegerField(default=0)
    revisitas = models.IntegerField(null=True, blank=True)
    cursos = models.IntegerField(null=True, blank=True)
    observaciones = models.IntegerField(null=True, blank=True)
    estado = models.CharField('Estado', choices=estado, max_length=100)    
    

    class Meta:
        verbose_name = "Informe Publicador"
        verbose_name_plural = "Informes Publicador"

    def __str__(self):
        return self.informe_mensual

