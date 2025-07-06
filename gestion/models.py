# -*- coding: utf-8 -*-
# Derechos de autor © 2025 Jhovany Calixto Luna. Todos los derechos reservados.

from django.db import models
from django.utils import timezone

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre

class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)
    raza = models.CharField(max_length=50)
    edad = models.IntegerField()
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} ({self.especie})"
    
class Consulta(models.Model):
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    motivo = models.CharField(max_length=200)
    diagnostico = models.TextField(blank=True, null=True)
    tratamiento = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)

# Campo para guardar PDF generado
    boleta_pdf = models.FileField(upload_to='boletas/', null=True, blank=True)

    def __str__(self):
        return f"Consulta {self.mascota.nombre} - {self.fecha}"