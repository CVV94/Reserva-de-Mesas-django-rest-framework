from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Modelo para representar la Mesa
class Mesa(models.Model):
    numero = models.IntegerField(unique=True)
    capacidad_personas = models.IntegerField()

    def __str__(self):
        return f"Mesa {self.numero} con capacidad de {self.capacidad_personas} persona/s"
    class Meta:
        db_table = 'Mesa'
        managed = True


# Modelo para representar el Estado de la Reserva
class EstadoReserva(models.TextChoices):
    RESERVADO = 'RESERVADO', 'Reservado'
    COMPLETADA = 'COMPLETADA', 'Completada'
    ANULADA = 'ANULADA', 'Anulada'
    NO_ASISTEN = 'NO_ASISTEN', 'No Asisten'

# Modelo para representar la Reserva
class Reserva(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_persona = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    fecha_reserva = models.DateField()
    hora_reserva = models.TimeField()
    cantidad_personas = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(15)])
    estado = models.CharField(
        max_length=20,
        choices=EstadoReserva.choices,
        default=EstadoReserva.RESERVADO,
    )
    mesa_asignada = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    observacion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reserva #{self.id} - {self.nombre_persona}"
    
    # Métodos para establecer campos obligatorios
    def save(self, *args, **kwargs):
        if not self.nombre_persona or not self.telefono or not self.fecha_reserva or not self.hora_reserva or not self.mesa_asignada:
            raise ValueError("Campo Obligatorio Vacío")
        if self.mesa_asignada.capacidad_personas < self.cantidad_personas:
            raise ValueError("La cantidad de personas supera la capacidad de la mesa")
        super().save(*args, **kwargs)


    class Meta:
        db_table = 'Reserva'
        managed = True