from django import forms
from .models import Order,OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['guest_name', 'guest_email', 'customer_address']  


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'customization']


class GuestCheckoutForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
