from django import forms
from .models import ShippingAddress, Order, Comment
from django.core.validators import MaxLengthValidator

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'state', 'zipcode']

class PlaceOrderForm(forms.Form):
    place_order = forms.BooleanField(widget=forms.HiddenInput, initial=True)

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['payment_method']

    payment_method = forms.ChoiceField(
                    choices=Order.PAYMENT_METHOD_CHOICES,
                    widget=forms.RadioSelect,)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
