from django.db import transaction
from django.shortcuts import render, redirect

from django.views.generic import View, TemplateView
from .models import Shipment, Category, Tax, Surcharge, ShipmentCategory, SurchargeShipment
from .forms import ShipmentForm, CategoryForm, TaxForm, SurchargeForm


class Home(TemplateView):
    def get(self, request):
        return render(request, 'home/home.html')


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
        surcharges = Surcharge.objects.filter(active=True)
        form = self.form_class()
        return render(request, self.template_name,
                      {'form': form, 'title': 'Crear Envío', 'categories': categories, 'surcharges': surcharges})

    # @transaction.atomic se utiliza para garantizar la integridad de la base de datos en situaciones
    # donde múltiples operaciones deben ejecutarse como una sola transacción para evitar inconsistencias en la base
    # de datos en caso de errores.
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        selected_categories = request.POST.getlist('categories')
        selected_surcharge = request.POST.getlist('surcharges')
        taxes = Tax.objects.filter(active=True)

        if form.is_valid():
            shipment = form.save()
            taxes = Shipment.defineTaxesByCategories(shipment, selected_categories, taxes)
            shipment.taxes = taxes
            shipment.final_price = Shipment.getTotalPrice(shipment)
            shipment.save()

            shipment_categories = [ShipmentCategory(shipment=shipment, category_id=category_id) for category_id in
                                   selected_categories]
            ShipmentCategory.objects.bulk_create(shipment_categories)

            shipment_surcharges = [SurchargeShipment(shipment=shipment, surcharge_id=surcharge_id) for surcharge_id in
                                   selected_surcharge]
            SurchargeShipment.objects.bulk_create(shipment_surcharges)
            return redirect('shipments')
        return render(request, self.template_name, {'form': form, 'title': 'Crear Envío'})


class EditShipment(View):
    model = Shipment
    template_name = 'posts/edit.html'
    form_class = ShipmentForm

    def get(self, request, *args, **kwargs):
        shipment = self.model.objects.get(pk=kwargs['id'])
        categories = Category.objects.all()
        surcharges = Surcharge.objects.filter(active=True)
        form = self.form_class(instance=shipment)
        return render(request, self.template_name, {'form': form, 'title': 'Editar Envío', 'categories': categories,
                                                    'surcharges': surcharges})

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        shipment = self.model.objects.get(pk=kwargs['id'])
        form = self.form_class(request.POST, instance=shipment)
        taxes = Tax.objects.filter(active=True)
        selected_categories = request.POST.getlist('categories')
        selected_surcharge = request.POST.getlist('surcharges')
        taxesToAdd = Shipment.defineTaxesByCategories(shipment, selected_categories, taxes)

        if form.is_valid():
            shipment.taxes = taxesToAdd
            shipment.final_price = Shipment.getTotalPrice(shipment)
            shipment = form.save()
            shipment.categories.clear()
            shipment.surcharges.clear()


            shipment_categories = [ShipmentCategory(shipment=shipment, category_id=category_id) for category_id in
                                   selected_categories]
            ShipmentCategory.objects.bulk_create(shipment_categories)

            shipment_surcharges = [SurchargeShipment(shipment=shipment, surcharge_id=surcharge_id) for surcharge_id in
                                   selected_surcharge]
            SurchargeShipment.objects.bulk_create(shipment_surcharges)
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
        return render(request, self.template_name, {'form': form, 'title': 'Crear recargo Arbitratio'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('settings')
        return render(request, self.template_name, {'form': form, 'title': 'Crear recargo Arbitrario'})


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


class GetQueries(View):
    model = Shipment

    def get(self, request):
        shipments = Shipment.objects.all()
        propicioAPerderse = Shipment.getTheLowestPriceFromShipmentDatabase(Shipment)


        return render(request, 'home/queries.html',
                      {'shipments': shipments, 'propicioAPerderse': propicioAPerderse})
