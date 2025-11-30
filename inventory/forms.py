from django import forms
from .models import Gemstone, InventoryMovement, EntryMovement, ExitMovement, AdjustmentMovement

class GemstoneForm(forms.ModelForm):
    class Meta:
        model = Gemstone
        fields = ["id", "name", "type"]

class EntryForm(forms.ModelForm):
    class Meta:
        model = EntryMovement
        fields = ["ammount"]

class ExitForm(forms.ModelForm):
    class Meta:
        model = ExitMovement
        fields = ["ammount", "destination"]

class AdjustmentForm(forms.ModelForm):
    class Meta:
        model = AdjustmentMovement
        fields = ["ammount", "motive"]
