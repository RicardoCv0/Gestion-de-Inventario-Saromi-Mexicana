from django import forms
from .models import Gemstone, EntryMovement, ExitMovement, AdjustmentMovement

class GemstoneForm(forms.ModelForm):
    class Meta:
        model = Gemstone
        fields = ["id", "name", "type"]

class EntryForm(forms.ModelForm):
    class Meta:
        model = EntryMovement

class ExitForm(forms.Form):
    class Meta:
        model = ExitMovement

class AdjustmentForm(forms.Form):
    class Meta:
        model = AdjustmentMovement
