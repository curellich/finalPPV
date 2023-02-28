from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View, TemplateView, CreateView
from .models import Shipment, Category, Tax, Surcharge, ShipmentCategory
from .forms import ShipmentForm, CategoryForm, TaxForm, SurchargeForm


class Home(TemplateView):
    def get(self, request):
        return render(request, 'pages/home.html')


"""Posts views"""


class GetShipments(View):
    def get(self, request):
        shipments = Shipment.objects.all()
        return render(request, 'posts/index.html',
                      {'shipments': shipments})


class CreateShipment(View):
    model = Shipment
    template_name = 'posts/create.html'
    form_class = ShipmentForm

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'title': 'Crear Envío', 'categories': categories})

    # @transaction.atomic se utiliza para garantizar la integridad de la base de datos en situaciones
    # donde múltiples operaciones deben ejecutarse como una sola transacción para evitar inconsistencias en la base
    # de datos en caso de errores.
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        selected_categories = request.POST.getlist('categories')
        if form.is_valid():
            shipment = form.save()
            shipment_categories = [ShipmentCategory(shipment=shipment, category_id=category_id) for category_id in
                                   selected_categories]
            ShipmentCategory.objects.bulk_create(shipment_categories)
            return redirect('shipments')
        return render(request, self.template_name, {'form': form, 'title': 'Crear Envío'})


class EditShipment(View):
    model = Shipment
    template_name = 'posts/edit.html'
    form_class = ShipmentForm

    def get(self, request, *args, **kwargs):
        shipment = self.model.objects.get(pk=kwargs['id'])
        categories = Category.objects.all()
        form = self.form_class(instance=shipment)
        return render(request, self.template_name, {'form': form, 'title': 'Editar Envío', 'categories': categories})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        shipment = self.model.objects.get(pk=kwargs['id'])
        form = self.form_class(request.POST, instance=shipment)
        selected_categories = request.POST.getlist('categories')
        if form.is_valid():
            shipment = form.save()
            shipment.categories.clear()
            shipment_categories = [ShipmentCategory(shipment=shipment, category_id=category_id) for category_id in
                                   selected_categories]
            ShipmentCategory.objects.bulk_create(shipment_categories)
            return redirect('shipments')
        return render(request, self.template_name, {'form': form, 'title': 'Editar Envío'})


class DeleteShipment(View):
    def get(self, request, id):
        shipment = Shipment.objects.get(pk=id)
        shipment.delete()
        return redirect('shipments')


"""Settings views"""


class GetSettings(View):
    def get(self, request):
        categories = Category.objects.all()
        taxes = Tax.objects.all()
        surcharges = Surcharge.objects.all()
        return render(request, 'settings/index.html',
                      {'categories': categories, 'taxes': taxes, 'surcharges': surcharges})


class CreateCategory(View):
    model = Category
    template_name = 'settings/create.html'
    form_class = CategoryForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'title': 'Crear Categoria'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('settings')
        return render(request, self.template_name, {'form': form, 'title': 'Crear categoría'})


class CreateTax(View):
    model = Tax
    template_name = 'settings/create.html'
    form_class = TaxForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'title': 'Crear impuesto'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('settings')
        return render(request, self.template_name, {'form': form, 'title': 'Crear impuesto'})


class CreateSurcharge(View):
    model = Surcharge
    template_name = 'settings/create.html'
    form_class = SurchargeForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, 'title': 'Crear recargo'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('settings')
        return render(request, self.template_name, {'form': form, 'title': 'Crear recargo'})


class EditCategory(View):
    model = Category
    template_name = 'settings/edit.html'
    form_class = CategoryForm

    def get(self, request, id):
        category = Category.objects.get(pk=id)
        form = self.form_class(instance=category)
        return render(request, self.template_name, {'form': form, 'title': 'Editar categoría'})

    def post(self, request, id):
        category = Category.objects.get(pk=id)
        form = self.form_class(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('settings')
        return render(request, self.template_name, {'form': form, 'title': 'Editar categoría'})


class EditTax(View):
    model = Tax
    template_name = 'settings/edit.html'
    form_class = TaxForm

    def get(self, request, id):
        tax = Tax.objects.get(pk=id)
        form = self.form_class(instance=tax)
        return render(request, self.template_name, {'form': form, 'title': 'Editar impuesto'})

    def post(self, request, id):
        tax = Tax.objects.get(pk=id)
        form = self.form_class(request.POST, instance=tax)
        if form.is_valid():
            form.save()
            return redirect('settings')
        return render(request, self.template_name, {'form': form, 'title': 'Editar impuesto'})


class EditSurcharge(View):
    model = Surcharge
    template_name = 'settings/edit.html'
    form_class = SurchargeForm

    def get(self, request, id):
        surcharge = Surcharge.objects.get(pk=id)
        form = self.form_class(instance=surcharge)
        return render(request, self.template_name, {'form': form, 'title': 'Editar Recargo'})

    def post(self, request, id):
        surcharge = Surcharge.objects.get(pk=id)
        form = self.form_class(request.POST, instance=surcharge)
        if form.is_valid():
            form.save()
            return redirect('settings')
        return render(request, self.template_name, {'form': form, 'title': 'Editar Recargo'})


class DeleteCategory(View):
    model = Category

    def get(self, request, id):
        category = Category.objects.get(pk=id)
        category.delete()
        return redirect('settings')


class DeleteTax(View):
    model = Tax

    def get(self, request, id):
        tax = Tax.objects.get(pk=id)
        tax.delete()
        return redirect('settings')


class DeleteSurcharge(View):
    model = Surcharge

    def get(self, request, id):
        surcharge = Surcharge.objects.get(pk=id)
        surcharge.delete()
        return redirect('settings')


"""Queries views"""


def queries(request):
    return render(request, 'pages/queries.html')
