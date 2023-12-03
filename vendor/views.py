from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from django.db.models import Avg, Count
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import *
from .serializers import *

# Create your views here.

class VendorListView(GenericAPIView):
    serializer_class = VendorSerializer
    pagination_class = PageNumberPagination

    def get(self,request):
        vendor_id = request.query_params.get('vendor_id')
        if vendor_id is None:
            obj = Vendor.objects.all().order_by('created_at')
            page = self.paginate_queryset(obj)
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            return Response({"message": "List of vendors retrieved successfully", "data": response.data}, 
                        status=status.HTTP_200_OK)
        else:
            try:
                obj = Vendor.objects.get(id=vendor_id)
            except Vendor.DoesNotExist:
                raise serializers.ValidationError({
                "error_message": "Invalid Vendor ID supplied!."
            })
            serializer = self.get_serializer(obj)
            return Response({"message": "Vendor retrieved successfully", "data": serializer.data}, 
                        status=status.HTTP_200_OK)

    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Vendor added successfully", "data": serializer.data}, 
                        status=status.HTTP_200_OK)

    def put(self, request):
        vendor_id = request.query_params.get('vendor_id')
        try:
            obj = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            raise serializers.ValidationError({
                "error_message": "Invalid Vendor ID supplied!."
            })
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Vendor updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request):
        vendor_id = request.query_params.get('vendor_id')
        try:
            obj = Vendor.objects.get(id=vendor_id)
        except Vendor.DoesNotExist:
            raise serializers.ValidationError({
                "error_message": "Invalid Vendor ID supplied!."
            })
        obj.delete()
        return Response({"message": "Vendor deleted successfully"}, status=status.HTTP_200_OK)

class PurchaseOrderListView(GenericAPIView):
    serializer_class = PurchaseOrderSerializer
    pagination_class = PageNumberPagination

    def get(self,request):
        po_id = request.query_params.get('po_id')
        if po_id is None:
            obj = PurchaseOrder.objects.all().order_by('created_at')
            page = self.paginate_queryset(obj)
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            return Response({"message": "List of POs retrieved successfully", "data": response.data}, 
                        status=status.HTTP_200_OK)
        else:
            try:
                obj = PurchaseOrder.objects.get(id=po_id)
            except PurchaseOrder.DoesNotExist:
                raise serializers.ValidationError({
                "error_message": "Invalid PO ID supplied!."
            })
            serializer = self.get_serializer(obj)
            return Response({"message": "PO retrieved successfully", "data": serializer.data}, 
                        status=status.HTTP_200_OK)

    def post(self,request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "PO added successfully", "data": serializer.data}, 
                        status=status.HTTP_200_OK)

    def put(self, request):
        po_id = request.query_params.get('po_id')
        try:
            obj = PurchaseOrder.objects.get(id=po_id)
        except PurchaseOrder.DoesNotExist:
            raise serializers.ValidationError({
                "error_message": "Invalid PO ID supplied!."
            })
        serializer = self.get_serializer(obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "PO updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)

    def delete(self, request):
        po_id = request.query_params.get('po_id')
        try:
            obj = PurchaseOrder.objects.get(id=po_id)
        except PurchaseOrder.DoesNotExist:
            raise serializers.ValidationError({
                "error_message": "Invalid PO ID supplied!."
            })
        obj.delete()
        return Response({"message": "PO deleted successfully"}, status=status.HTTP_200_OK)


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