from rest_framework import serializers
from .models import Vendor, PurchaseOrder


class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = [
            'id', 'name', 'contact_details', 'address', 'vendor_code',
            'on_time_delivery_rate', 'quality_rating_avg',
            'average_response_time', 'fulfillment_rate'
        ]
        extra_kwargs = {
            'name': {'required': True},
            'contact_details': {'required': True},
            'address': {'required': True},
            'vendor_code': {'required': True},
            # The following fields are not required and will default to 0.0 if not provided
            'on_time_delivery_rate': {'required': False, 'default': 0.0},
            'quality_rating_avg': {'required': False, 'default': 0.0},
            'average_response_time': {'required': False, 'default': 0.0},
            'fulfillment_rate': {'required': False, 'default': 0.0},
        }


class PurchaseOrderSerializer(serializers.ModelSerializer):
    vendor_name = serializers.ReadOnlyField(source='vendor.name')  # Add a read-only field for vendor name

    class Meta:
        model = PurchaseOrder
        fields = '__all__'

    def validate_quantity(self, value):
        """
        Validate that the quantity is a positive integer.
        """
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive integer.")
        return value

    def create(self, validated_data):
        """
        Override create method to include custom behavior.
        For example, you can perform additional actions before or after creating the purchase order.
        """
        # Perform additional actions before creating the purchase order
        return PurchaseOrder.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Override update method to include custom behavior.
        For example, you can perform additional actions before or after updating the purchase order.
        """
        # Perform additional actions before updating the purchase order
        instance = super().update(instance, validated_data)
        # Perform additional actions after updating the purchase order
        return instance


class VendorPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['on_time_delivery_rate', 'quality_rating_avg', 'average_response_time', 'fulfillment_rate']
