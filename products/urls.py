from django.urls import path
from . import views

urlpatterns = [
    path('newProduct', views.newProduct, name='newProduct'),
    path('editProduct/<int:product_id>/',views.editProduct,name='editProduct'),
    path('createVariation/<int:product_id>/',views.createVariation,name='createVariation'),

]