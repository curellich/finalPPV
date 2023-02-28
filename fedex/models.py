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
    amount = models.DecimalField(max_digits=10, null=True, decimal_places=2, verbose_name='Surcharge Amount')
    active = models.BooleanField(default=False)

    class Meta:
        db_table = 'surcharges'


class ShipmentCategory(models.Model):
    shipment = models.ForeignKey('Shipment', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = 'shipment_categories'


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
    surcharges = models.ManyToManyField(Surcharge, through=SurchargeShipment)
    taxes = models.DecimalField(max_digits=9, null=True, default=0.00, decimal_places=2,
                                verbose_name='Taxes')
    final_price = models.DecimalField(max_digits=9, null=True, default=0.00, decimal_places=2,
                                      verbose_name='Final Price')

    def __str__(self):
        return self.code

    class Meta:
        db_table = 'shipments'

    def getTheLowestPriceFromShipmentDatabase(self):
        return self.objects.all().order_by('final_price').first()

    def getWeight(self):
        return self.weight

    def getCategories(self):
        return self.categories.all()

    def getSurcharges(self):
        return self.surcharges.all()

    def getTaxes(self):
        return self.taxes

    def calculateSurcharges(self, surcharges):
        total = 0
        categories = self.getCategories()

        for category in categories:
            total += category.surcharge_percentage * self.base_price / 100

        weight = self.getWeight()
        if weight > 1:
            total += 80

        for surcharge in self.getSurcharges():
            total += surcharge.amount

        return total

    def defineTaxesByCategories(self, selected_categories, taxes):
        surcharges = self.calculateSurcharges(self.getSurcharges())
        netoPrice = self.base_price + surcharges
        total = 0

        try:
            tax = taxes.get(name='IVA')
            total += tax.percentage * netoPrice / 100
        except Tax.DoesNotExist:
            pass

        if len(selected_categories) > 3:
            try:
                tax = taxes.get(name='Multicategoria')
                total += tax.percentage * netoPrice / 100
            except Tax.DoesNotExist:
                pass

        if self.isInternational():
            try:
                tax = taxes.get(name='Aduanero')
                total += tax.percentage * netoPrice / 100
            except Tax.DoesNotExist:
                pass

        if self.isBasePriceOdd():
            try:
                tax = taxes.get(name='Extraño')
                total += tax.percentage * netoPrice / 100
            except Tax.DoesNotExist:
                pass

        if self.isNational():
            try:
                tax = taxes.get(name='Municipal')
                total += tax.percentage * netoPrice / 100
            except Tax.DoesNotExist:
                pass

        return total

    def isInternational(self):
        return self.origin_country != self.destination_country

    def isBasePriceOdd(self):
        return self.base_price % 2 != 0

    def isNational(self):
        return self.origin_country == self.destination_country and self.origin_city != self.destination_city

    def getTotalPrice(self):
        return round((self.base_price + self.taxes + self.calculateSurcharges(self.getSurcharges())), 2)

