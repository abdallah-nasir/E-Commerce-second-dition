import django_filters
from django import forms
from .models import *

PRODUCT_CHOICES=(
    ("1","1"),
    ("2","2"),
    ("3","3"),
    ("4","4"),
    ("5","5"),
)
class ProductFilter(django_filters.FilterSet):
    price=django_filters.CharFilter(lookup_expr='icontains')
    # range=django_filters.CharFilter(field_name='price 2',lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['price']   
