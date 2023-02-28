from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('settings', views.getAllSettings, name='settings'),
    path('shipments', views.getShipments, name='shipments'),
    path('queries', views.queries, name='queries'),
    path('shipments/create', views.createShipment, name='createShipment'),
    path('shipments/edit/<int:id>', views.editShipment, name='editShipment'),
    path('post/delete/<int:id>', views.deleteShipment, name='deleteShipment'),
    path('settings/createCategory', views.createCategory, name='createCategory'),
    path('settings/createTax', views.createTax, name='createTax'),
    path('settings/createSurcharge', views.createSurcharge, name='createSurcharge'),
    path('category/edit/<int:id>', views.editCategory, name='editCategory'),
    path('tax/edit/<int:id>', views.editTax, name='editTax'),
    path('settings/edit/<int:id>', views.editSurcharge, name='editSurcharge'),
    path('category/delete/<int:id>', views.deleteCategory, name='deleteCategory'),
    path('tax/delete/<int:id>', views.deleteTax, name='deleteTax'),
    path('surcharge/delete/<int:id>', views.deleteSurcharge, name='deleteSurcharge'),

]