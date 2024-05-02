from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .custom_response import CustomMetaDataMixin
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer
from .utils import recalculate_average_response_time, calculate_vendor_performance
from django.utils import timezone
from rest_framework import status
import logging


logger = logging.getLogger(__name__)

# Create your views here.


class VendorPing(CustomMetaDataMixin, APIView):
    def get(self, request):  # noqa
        return Response("Pong")


class VendorView(CustomMetaDataMixin, APIView):
    def post(self, request):
        try:
            serializer = VendorSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                serializer.save()
                return Response("New Vendor Created.", status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(print(f"Logout error: {e.__str__()}, data: {request.data}"))
            return Response(e.__str__(), status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, vendor_id=None):
        """
        Get Vendor details All ('http://localhost:8666/api/vendors/')
        + A Particular Lender Detail ('http://localhost:8666/api/vendors/1/')
        """
        if vendor_id:
            vendor = Vendor.objects.filter(id=vendor_id).first()
            if vendor:
                return Response({
                    'name': vendor.name,
                    'contact_details': vendor.contact_details,
                    'address': vendor.address,
                    'vendor_code': vendor.vendor_code,
                    'on_time_delivery_rate': vendor.on_time_delivery_rate,
                    'quality_rating_avg': vendor.quality_rating_avg,
                    'average_response_time': vendor.average_response_time,
                    'fulfillment_rate': vendor.fulfillment_rate
                }, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Vendor not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            vendors = list(Vendor.objects.values(
                'name', 'contact_details', 'address', 'vendor_code',
                'on_time_delivery_rate', 'quality_rating_avg',
                'average_response_time', 'fulfillment_rate'))
            return Response(vendors)

    def put(self, request, vendor_id):
        """
        Update Any detail on Vendor Info.
        """
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            serializer = VendorSerializer(vendor, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Vendor updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=400)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, vendor_id):
        """
        Delete Vendor.
        """
        try:
            vendor = Vendor.objects.get(id=vendor_id)
            vendor.delete()
            return Response({'message': 'Vendor deleted successfully'}, status=status.HTTP_200_OK)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VendorPerformance(CustomMetaDataMixin, generics.RetrieveAPIView):
    """
    Vendor Performance Detail ('vendors/<int:pk>/performance/')
    """
    permission_classes = (IsAuthenticated,)
    queryset = Vendor.objects.all()
    serializer_class = VendorPerformanceSerializer

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # import pdb;pdb.set_trace()
            performance_metrics = calculate_vendor_performance(instance.id)
            serializer = self.get_serializer(performance_metrics)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderListCreate(CustomMetaDataMixin, APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            purchase_order = list(PurchaseOrder.objects.values().all())
            return Response(purchase_order)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderRetrieveUpdateDestroy(CustomMetaDataMixin, APIView):
    permission_classes = (IsAuthenticated,)
    def get_object(self, pk):
        purchase_order_obj = PurchaseOrder.objects.filter(pk=pk).last()
        assert purchase_order_obj, f"Purchase Order ID {pk} is not in Database"
        return purchase_order_obj

    def get(self, request, pk):
        try:
            purchase_order = self.get_object(pk)
            serializer = PurchaseOrderSerializer(purchase_order)
            return Response(serializer.data)
        except Exception as e:
            return Response(e.__str__(), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        purchase_order = self.get_object(pk)
        serializer = PurchaseOrderSerializer(purchase_order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            purchase_order = self.get_object(pk)
            purchase_order.delete()
            return Response("OK. Purchase Order has being deleted", status=status.HTTP_200_OK)
        except Exception as e:
            return Response(e.__str__(), status=status.HTTP_400_BAD_REQUEST)


class AcknowledgePurchaseOrder(CustomMetaDataMixin, APIView):
    """
    This endpoint will update acknowledgment_date and trigger the recalculation
    of average_response_time.
    """
    permission_classes = (IsAuthenticated,)
    def post(self, request, po_id):
        purchase_order = get_object_or_404(PurchaseOrder, pk=po_id)
        purchase_order.acknowledgment_date = timezone.now()
        purchase_order.save()
        # Update average response time for vendor
        recalculate_average_response_time(purchase_order.vendor)
        return Response({'message': 'Purchase Order acknowledged successfully.'})
