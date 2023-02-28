from django import forms
from .models import Shipment, Category, Tax, Surcharge
from django.forms.fields import Field

setattr(Field, 'is_checkbox', lambda self: isinstance(self.widget, forms.CheckboxInput))


class ShipmentForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = 'id', 'code', 'origin_city', 'origin_country', 'destination_city', 'destination_country', 'weight',\
            'base_price'


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
