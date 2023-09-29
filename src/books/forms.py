from django import forms
from .models import ShippingAddress

# class CartAddForm(forms.Form):
#     quantity = forms.IntegerField(initial=1, min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))

# class CartUpdateForm(forms.Form):
#     quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'state', 'zipcode']

class PlaceOrderForm(forms.Form):
    place_order = forms.BooleanField(widget=forms.HiddenInput, initial=True)