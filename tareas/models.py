from django.db import models


class Tarea(models.Model):
    ESTADOS = [("pendiente", "Pendiente"), ("completada", "Completada")]

    titulo = models.CharField(max_length=150)
    curso = models.CharField(max_length=100)
    fechaEntrega = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default="pendiente")

    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "curso": self.curso,
            "fechaEntrega": self.fechaEntrega.isoformat(),
            "estado": self.estado,
        }

    def __str__(self):
        return self.titulo
