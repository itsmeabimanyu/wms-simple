from django.shortcuts import redirect
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', lambda request: redirect('warehouseview')),
    path('dashboard/', views.Dashboard.as_view(), name='dashboard'),
    path('warehouse/', views.ViewWarehouse.as_view(), name='warehouse'),
    path('warehouse/view/', views.CreateWarehouse.as_view(), name='warehouseview'),
    path('warehouse/edit/<uuid:pk>/', views.UpdateWarehouse.as_view(), name='warehouseupdate'),
]