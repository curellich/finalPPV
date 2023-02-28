from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150, verbose_name='name')
    surcharge_percentage = models.DecimalField(max_digits=9, default=0.00, decimal_places=2,
                                               verbose_name='Surcharge Percentage')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'categories'


class Tax(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Tax Name')
    percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Tax Percentage')
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'taxes'


class Surcharge(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Surcharge Name')
    percentage = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Surcharge Percentage')
    amount = models.DecimalField(max_digits=10, null=True, decimal_places=2, verbose_name='Surcharge Amount')
    active = models.BooleanField(default=False)

    class Meta:
        db_table = 'surcharges'


class ShipmentCategory(models.Model):
    shipment = models.ForeignKey('Shipment', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'shipment_categories'


class TaxShipment(models.Model):
    tax = models.ForeignKey(Tax, on_delete=models.CASCADE)
    shipment = models.ForeignKey('Shipment', on_delete=models.CASCADE)

    class Meta:
        db_table = 'shipment_taxes'


class SurchargeShipment(models.Model):
    surcharge = models.ForeignKey(Surcharge, on_delete=models.CASCADE)
    shipment = models.ForeignKey('Shipment', on_delete=models.CASCADE)

    class Meta:
        db_table = 'shipment_surcharges'


class Shipment(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True, verbose_name='Shipment Code')
    origin_city = models.CharField(max_length=150, verbose_name='Origin City')
    origin_country = models.CharField(max_length=150, verbose_name='Origin Country')
    destination_city = models.CharField(max_length=150, verbose_name='Destination City')
    destination_country = models.CharField(max_length=150, verbose_name='Destination Country')
    weight = models.DecimalField(max_digits=9, default=0.00, decimal_places=2)
    base_price = models.DecimalField(max_digits=9, default=0.00, decimal_places=2, verbose_name='Base Price')
    categories = models.ManyToManyField(Category, through=ShipmentCategory)
    taxes = models.ManyToManyField(Tax, through=TaxShipment)
    surcharges = models.ManyToManyField(Surcharge, through=SurchargeShipment)

    def __str__(self):
        return self.code

    def save(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(Shipment, self).save(*args, **kwargs)
        categories = request.POST.getlist('categories')
        for category_id in categories:
            category = Category.objects.get(pk=category_id)
            ShipmentCategory.objects.create(shipment=self, category=category)

    class Meta:
        db_table = 'shipments'

    def getCategories(self):
        return self.categories.all()

    def getTaxes(self):
        return self.taxes.all()

    def getSurcharges(self):
        return self.surcharges.all()

    def getTotalPrice(self):
        return self.base_price + 1000
