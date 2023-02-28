from django import forms
from .models import Shipment, Category, Tax, Surcharge
from django.forms.fields import Field

setattr(Field, 'is_checkbox', lambda self: isinstance(self.widget, forms.CheckboxInput))


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = 'id', 'code', 'origin_city', 'origin_country', 'destination_city', 'destination_country', 'weight', \
            'base_price'
        labels = {
            'id': 'ID',
            'code': 'Shipment Code',
            'origin_city': 'Origin City',
            'origin_country': 'Origin Country',
            'destination_city': 'Destination City',
            'destination_country': 'Destination Country',
            'weight': 'Weight',
            'base_price': 'Base Price',
            'categories': 'Categories'
        }



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class TaxForm(forms.ModelForm):
    class Meta:
        model = Tax
        fields = '__all__'


class SurchargeForm(forms.ModelForm):
    class Meta:
        model = Surcharge
        fields = '__all__'
