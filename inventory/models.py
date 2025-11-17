from django.db import models

class Gemstone(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    type = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    ammount_available = models.DecimalField(max_digits=20, decimal_places=5, default=0)

class InventoryMovement(models.Model):
    gemstone = models.ForeignKey(Gemstone, on_delete=models.DO_NOTHING)
    ammount = models.DecimalField(max_digits=20, decimal_places=5)
    date_time = models.DateTimeField()
    responsible = models.CharField(max_length=100)

class EntryMovement(InventoryMovement):
    pass

class ExitMovement(InventoryMovement):
    destination = models.CharField(max_length=200)

class AdjustmentMovement(InventoryMovement):
    motive = models.CharField(max_length=200)
