from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('newProduct', views.newProduct, name='newProduct'),
    path('viewProducts', views.viewProducts, name='viewProducts'),
    path('editProduct/<int:product_id>/',views.editProduct,name='editProduct'),
    path('createVariation/<int:product_id>/',views.createVariation,name='createVariation'),
    path('createImage/<int:product_id>/',views.createImage,name='createImage'),
    path('viewCatalogs', views.viewCatalogs, name='viewCatalogs'),
    path('addCategory', views.addCategory, name='addCategory'),
    path('getCategoryById/<int:id>/', views.getCategoryById, name='getCategoryById'),

]