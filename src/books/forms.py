from django import forms
from .models import ShippingAddress

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'state', 'zipcode']

class PlaceOrderForm(forms.Form):
    place_order = forms.BooleanField(widget=forms.HiddenInput, initial=True)