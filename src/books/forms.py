from django import forms
from .models import ShippingAddress, Order, Comment
from django.core.validators import MaxLengthValidator

class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['address', 'city', 'state', 'zipcode']

class PlaceOrderForm(forms.Form):
    place_order = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class BookFilterForm(forms.Form):
    author = forms.CharField(
        required=False,
        label='',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Author'})
    )
    min_price = forms.DecimalField(
        required=False,
        label='',
        min_value=0,  
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'placeholder': 'Min Price'}))
    max_price = forms.DecimalField(
        required=False,
        label='',
        min_value=0, 
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'placeholder': 'Max Price'})
    )
    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')

        if min_price is not None and max_price is not None and min_price > max_price:
            raise forms.ValidationError("Minimum price should be less than or equal to maximum price.")

        return cleaned_data

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
