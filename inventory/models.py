from django.db import models

class Gemstone(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    ammount_available = models.DecimalField(max_digits=20, decimal_places=5, default=0)

MOVEMENT_TYPES = [
    ("entry", "Entrada"),
    ("exit", "Salida"),
    ("adjustment", "Ajuste"),
]

class InventoryMovement(models.Model):
    gemstone = models.ForeignKey(Gemstone, on_delete=models.DO_NOTHING)
    ammount = models.DecimalField(max_digits=20, decimal_places=5)
    date_time = models.DateTimeField()
    responsible = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=MOVEMENT_TYPES, default="entry")

class EntryMovement(InventoryMovement):
    pass

DESTINATIONS = [
    ("prod", "Producción"),
    ("sales", "Ventas"),
]

ADJUSTMENT_MOTIVES = [
    ("damage", "Daño"),
    ("loss", "Pérdida"),
    ("regulation", "Regulación IMMEX"),
]

class ExitMovement(InventoryMovement):
    destination = models.CharField(max_length=20, choices=DESTINATIONS)

class AdjustmentMovement(InventoryMovement):
    motive = models.CharField(max_length=20, choices=ADJUSTMENT_MOTIVES)
