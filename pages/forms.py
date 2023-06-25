from django import forms
from .models import BbCodeModel
class BbCodeForm(forms.ModelForm):
    class Meta:
        model = BbCodeModel
        fields = '__all__'