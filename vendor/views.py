from django.shortcuts import render
from rest_framework import generics
from django.db.models import Avg, Count
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *

# Create your views here.

class VendorListView(generics.ListCreateAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class VendorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer

class PurchaseOrderListView(generics.ListCreateAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

class PurchaseOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

@api_view(['GET'])
def vendor_performance(request, vendor_id):
    vendor = Vendor.objects.get(pk=vendor_id)

    # Calculate performance metrics
    on_time_delivery_rate = vendor.purchaseorder_set.filter(status='completed', delivery_date__lte=timezone.now()).count() / vendor.purchaseorder_set.filter(status='completed').count() * 100
    quality_rating_avg = vendor.purchaseorder_set.filter(status='completed').aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0
    average_response_time = vendor.purchaseorder_set.filter(acknowledgment_date__isnull=False).aggregate(Avg('acknowledgment_date' - 'issue_date'))['acknowledgment_date__avg'] or 0
    fulfillment_rate = vendor.purchaseorder_set.filter(status='completed').count() / vendor.purchaseorder_set.all().count() * 100

    # Update vendor performance metrics
    vendor.on_time_delivery_rate = on_time_delivery_rate
    vendor.quality_rating_avg = quality_rating_avg
    vendor.average_response_time = average_response_time
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()

    serializer = VendorSerializer(vendor)
    return Response(serializer.data)