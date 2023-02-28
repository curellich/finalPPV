from django.shortcuts import render, redirect
from django.views.generic import View

from .models import Shipment, Category, Tax, Surcharge
from .forms import ShipmentForm, CategoryForm, TaxForm, SurchargeForm


# Create your views here.

# def home(request):
#     return render(request, 'pages/home.html')

class Home(View):
    def get(self, request):
        return render(request, 'pages/home.html')


"""Posts views"""


def getShipments(request):
    shipments = Shipment.objects.all()
    return render(request, 'posts/index.html',
                  {'shipments': shipments})


def createShipment(request):
    form = ShipmentForm(request.POST or None)
    categories = Category.objects.all()
    if form.is_valid():
        shipment = form.save(commit=False)
        shipment.save()  # Call the save method on the Shipment model instance
        form.save_m2m()
        return redirect('shipments')
    return render(request, 'posts/create.html',
                  {'form': form, 'title': 'Crear Envío', 'categories': categories})


def editShipment(request, id):
    shipment = Shipment.objects.get(id=id)
    form = ShipmentForm(request.POST or None, instance=shipment)
    categories = Category.objects.all()
    if form.is_valid() and request.POST:
        shipment = form.save(commit=False)
        shipment.save()  # Call the save method on the Shipment model instance
        form.save_m2m()
        return redirect('shipments')
    return render(request, 'posts/edit.html', {'form': form, 'title': 'Editar Envío', 'categories': categories})

# class EditShipment(UpdateView):
#     model = Shipment
#     template_name = 'posts/edit.html'
#     form_class = ShipmentForm
#     success_url = reverse_lazy('shipments')


def deleteShipment(request, id):
    shipment = Shipment.objects.get(id=id)
    shipment.delete()
    return redirect('shipments')


"""Settings views"""


def getAllSettings(request):
    categories = Category.objects.all()
    taxes = Tax.objects.all()
    surcharges = Surcharge.objects.all()
    return render(request, 'settings/index.html', {'categories': categories, 'taxes': taxes, 'surcharges': surcharges})


def createCategory(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('settings')
    return render(request, 'settings/create.html', {'form': form, 'title': 'Crear categoría'})


def createTax(request):
    form = TaxForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('settings')
    return render(request, 'settings/create.html', {'form': form, 'title': 'Crear impuesto'})


def createSurcharge(request):
    form = SurchargeForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('settings')
    return render(request, 'settings/create.html', {'form': form, 'title': 'Crear recargo'})


def editCategory(request, id):
    category = Category.objects.get(id=id)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid() and request.POST:
        form.save()
        return redirect('settings')
    return render(request, 'settings/edit.html', {'form': form, 'title': 'Editar categoría'})


def editTax(request, id):
    tax = Tax.objects.get(id=id)
    form = TaxForm(request.POST or None, instance=tax)
    if form.is_valid() and request.POST:
        form.save()
        return redirect('settings')
    return render(request, 'settings/edit.html', {'form': form, 'title': 'Editar impuesto'})


def editSurcharge(request, id):
    surcharge = Surcharge.objects.get(id=id)
    form = SurchargeForm(request.POST or None, instance=surcharge)
    if form.is_valid() and request.POST:
        form.save()
        return redirect('settings')
    return render(request, 'settings/edit.html', {'form': form, 'title': 'Editar recargo'})


def deleteCategory(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('settings')


def deleteTax(request, id):
    tax = Tax.objects.get(id=id)
    tax.delete()
    return redirect('settings')


def deleteSurcharge(request, id):
    surcharge = Surcharge.objects.get(id=id)
    surcharge.delete()
    return redirect('settings')


"""Queries views"""


def queries(request):
    return render(request, 'pages/queries.html')
