from django import template

register = template.Library()

@register.filter
def calculate_subtotal(cart_item):
    return cart_item.quantity * cart_item.books.price
