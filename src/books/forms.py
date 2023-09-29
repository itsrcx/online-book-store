from django import forms
from .models import ShippingAddress

# class CartAddForm(forms.Form):
#     quantity = forms.IntegerField(initial=1, min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))

# class CartUpdateForm(forms.Form):
#     quantity = forms.IntegerField(min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))


class CheckoutForm(forms.Form):
    shipping_address = forms.CharField(max_length=200)
    payment_method = forms.ChoiceField(choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')])

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'state', 'zipcode']