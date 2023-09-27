from django import forms
from .models import Cart

class UpdateCartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['quantity']

