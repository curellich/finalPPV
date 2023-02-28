from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('settings', GetSettings.as_view(), name='settings'),
    path('shipments', GetShipments.as_view(), name='shipments'),
    path('queries', GetQueries.as_view(), name='queries'),
    path('shipments/create', CreateShipment.as_view(), name='createShipment'),
    path('shipments/edit/<int:id>', EditShipment.as_view(), name='editShipment'),
    path('shipments/delete/<int:id>', DeleteShipment.as_view(), name='deleteShipment'),
    path('settings/createCategory', CreateCategory.as_view(), name='createCategory'),
    path('settings/createTax', CreateTax.as_view(), name='createTax'),
    path('settings/createSurcharge', CreateSurcharge.as_view(), name='createSurcharge'),
    path('category/edit/<int:id>', EditCategory.as_view(), name='editCategory'),
    path('tax/edit/<int:id>', EditTax.as_view(), name='editTax'),
    path('settings/edit/<int:id>', EditSurcharge.as_view(), name='editSurcharge'),
    path('category/delete/<int:id>', DeleteCategory.as_view(), name='deleteCategory'),
    path('tax/delete/<int:id>', DeleteTax.as_view(), name='deleteTax'),
    path('surcharge/delete/<int:id>', DeleteSurcharge.as_view(), name='deleteSurcharge'),

]