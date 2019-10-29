"""SaliknetaPOSIS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('salikneta/', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('signout', views.signout, name='signout'),
    path('log_in/', views.log_in, name='log_in'),
    path('verify/', views.log_in_validate, name='verify'),
    path('register/', views.register, name='register'),
    path('register_validate/', views.register_validate, name='register_validate'),
    path('manageCategories/', views.manageCategories, name='manageCategories'),
    path('manageSuppliers/', views.manageSuppliers, name='manageSuppliers'),
    path('manageItems/<int:id>', views.manageItems, name='manageItems'),
    path('manageRawMaterials/', views.manageRawMaterials, name='manageRawMaterials'),
    path('manageIngredients/<str:id>', views.manageIngredients, name='manageIngredients'),
    path('editItemPrice/', views.editItemPrice, name='editItemPrice'),
    path('editMaterialStock/', views.editMaterialStock, name='editMaterialStock'),
    path('purchaseOrder/', views.purchaseOrder, name='purchaseOrder'),
    path('backload/', views.backload, name='backload'),
    path('transferOrderProducts/', views.transferOrderProducts, name='transferOrderProducts'),
    path('transferOrderRawMaterials/', views.transferOrderRawMaterials, name='transferOrderRawMaterials'),
    path('produceItems/<str:id>', views.produceItems, name='produceItems'),
    path('pos/', views.pos, name='pos'),
    path('sales/', views.sales, name='sales'),
    path('forecasting/product=<int:id>method=<str:method>', views.forecasting_detail, name='forecasting_detail'),
    path('forecasting/method=<str:method>', views.forecasting, name='forecasting'),
    path('sales_report/', views.sales_report, name='sales_report'),
    path('sales_report_detail/', views.sales_report_detail, name='sales_report_detail'),

    path('inventory_report/', views.inventory_report, name='inventory_report'),
    path('inventory_report_detail/', views.inventory_report_detail, name='inventory_report_detail'),

    path('check_notifs/', views.check_notif, name='check_notifs'),
    path('open_notifs/', views.open_notif, name='open_notifs'),
    path('notifications/', views.notifications, name='notifications'),

    path('get_num_low_items/', views.get_num_lowstock, name='get_num_lowstock'),
    path('ajax/get_invoicelines_by_salesid/<int:idSales>/', views.get_invoice_by_id, name='get_invoicelines_by_salesid'),
    path('ajax/ajaxAddCategory/', views.ajaxAddCategory, name='ajaxAddCategory'),
    path('ajax/ajaxGetUpdatedCategories/', views.ajaxGetUpdatedCategories, name='ajaxGetUpdatedCategories'),
    path('ajax/ajaxAddSupplier/', views.ajaxAddSupplier, name='ajaxAddSupplier'),
    path('ajax/ajaxGetUpdatedSuppliers/', views.ajaxGetUpdatedSuppliers, name='ajaxGetUpdatedSuppliers'),
    path('ajax/ajaxAddItem/', views.ajaxAddItem, name='ajaxAddItem'),
    path('ajax/ajaxGetUpdatedItems/', views.ajaxGetUpdatedItems, name='ajaxGetUpdatedItems'),
    path('ajax/ajaxGetInStock/', views.ajaxGetInStock, name='ajaxGetInStock'),
    path('ajax/ajaxGetInStockProduct/', views.ajaxGetInStockProduct, name='ajaxGetInStockProduct'),
    path('ajax/ajaxGetDestinationStock/', views.ajaxGetDestinationStock, name='ajaxGetDestinationStock'),
    path('ajax/ajaxGetInStockRawMaterials/', views.ajaxGetInStockRawMaterials, name='ajaxGetInStockRawMaterials'),
    path('ajax/ajaxAddPurchaseOrder/', views.ajaxAddPurchaseOrder, name='ajaxAddPurchaseOrder'),
    path('ajax/ajaxAddBackload/', views.ajaxAddBackload, name='ajaxAddBackload'),
    path('ajax/ajaxSaveDelivery/', views.ajaxSaveDelivery, name='ajaxSaveDelivery'),
    path('ajax/ajaxTransferOrder/', views.ajaxTransferOrder, name='ajaxTransferOrder'),
    path('ajax/ajaxTransferOrderRawMaterials/', views.ajaxTransferOrderRawMaterials, name='ajaxTransferOrderRawMaterials'),
    path('ajax/ajaxInTransitTO/', views.ajaxInTransitTO, name='ajaxInTransitTO'),
    path('ajax/ajaxInTransitTORawMaterial/', views.ajaxInTransitTORawMaterial, name='ajaxInTransitTORawMaterial'),
    path('ajax/ajaxFinishedTO/', views.ajaxFinishedTO, name='ajaxFinishedTO'),
    path('ajax/ajaxFinishedTORawMaterial/', views.ajaxFinishedTORawMaterial, name='ajaxFinishedTORawMaterial'),
    path('ajax/ajaxCancelTO/', views.ajaxCancelTO, name='ajaxCancelTO'),
    path('ajax/ajaxCancelTORawMaterial/', views.ajaxCancelTORawMaterial, name='ajaxCancelTORawMaterial'),
    path('ajax/ajaxGetIngredients/', views.ajaxGetIngredients, name='ajaxGetIngredients'),
    path('ajax/ajaxGetBatches/', views.ajaxGetBatches, name='ajaxGetBatches'),
    path('ajax/ajaxGetUOM/', views.ajaxGetUOM, name='ajaxGetUOM'),
    path('ajax/ajaxAddIngredient/', views.ajaxAddIngredient, name='ajaxAddIngredient'),
    path('ajax/ajaxRemoveIngredient/', views.ajaxRemoveIngredient, name='ajaxRemoveIngredient'),
    path('ajax/ajaxGetAmountCanProduce/', views.ajaxGetAmountCanProduce, name='ajaxGetAmountCanProduce'),
    path('ajax/ajaxProduceItems/', views.ajaxProduceItems, name='ajaxProduceItems'),
    path('ajax/ajaxGetRawMaterialCountLogs/', views.ajaxGetRawMaterialCountLogs, name='ajaxGetRawMaterialCountLogs'),


    path('get/', views.get, name='get'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)