from django.urls import path
from .views import *

urlpatterns = [
    path('vendors/', VendorListView.as_view(), name='vendor-list'),
    path('vendors/<int:vendor_id>/', VendorListView.as_view(), name='vendor-detail'),
    path('purchase_orders/', PurchaseOrderListView.as_view(), name='purchase-order-list'),
    path('purchase_orders/<int:po_id>/', PurchaseOrderListView.as_view(), name='purchase-order-detail'),
    path('vendors/<int:vendor_id>/performance/', VendorPerformanceView.as_view(), name='vendor-performance'),
    path('purchase_orders/<int:po_id>/acknowledge/', AcknowledgePurchaseOrderView.as_view(), name='acknowledge-purchase-order'),
    path('vendors/<int:vendor_id>/historical_performance/', vendor_performance, name='vendor-historical-performance'),

]