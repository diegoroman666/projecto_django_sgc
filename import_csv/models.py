from django.db import models

class Usuario(models.Model):
    nombre_usuario = models.TextField(max_length=15)
    password_usuario = models.TextField(max_length=20)

    def __str__(self):
        return str(self.nombre_usuario) + " - " + str(self.password_usuario) 

class Correspondencia(models.Model):
    
    fecha = models.TextField(max_length=50)
    fechadocumento = models.TextField(max_length=50)
    folio = models.TextField(max_length=50)
    foliooficina = models.TextField(max_length=50)
    remitente = models.TextField(max_length=50)
    tipodocumento =  models.TextField(max_length=50)
    detalle = models.TextField(max_length=50)
    destino = models.TextField(max_length=50)
    resolucion =  models.TextField(max_length=50)
    fechadespacho= models.TextField(max_length=50)

    def __str__(self):
        return str(self.fecha) + " - " + str(self.fechadocumento)+ " - " + str(self.folio)+ " - " + str(self.foliooficina)+ " - " + str(self.remitente)+ " - " + str(self.tipodocumento)+ " - " + str(self.detalle)+ " - " + str(self.destino)+ " - " + str(self.resolucion)+ " - " + str(self.fechadespacho)

class Historial(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    descripcion_historial = models.TextField(max_length=200)
    tabla_afectada_historial = models.TextField(max_length=100)
    fecha_hora_historial = models.DateTimeField()

    def __str__(self):
        return str(self.usuario) + " - " + str(self.descripcion_historial)  + " - " + str(self.tabla_afectada_historial)  + " - " + str(self.fecha_hora_historial) 