from django.db import models

# Create your models here.

# NOTE :: As per Docs,
# These models form the backbone of the Vendor Management System, enabling
# comprehensive tracking and analysis of vendor performance over time. The performance
# metrics are updated based on interactions recorded in the Purchase Order model


class Vendor(models.Model):
    """
    Vendor Model to store vendor information including name, contact
    details, address, and a unique vendor code.
    This model stores essential information about each vendor and their performance metrics.
    """
    name = models.CharField(max_length=100)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    class Meta:
        db_table = "vendor"
        app_label = "vendors"

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    """
    Lets track purchase orders with fields like PO number, vendor reference,
    order date, items, quantity, and status.
    This model captures the details of each purchase order and is used to calculate various
    performance metrics.
    """
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "purchase_order"

    def __str__(self):
        return {"PurchaseOrder": self.po_number}


class HistoricalPerformance(models.Model):
    """
    HistoricalPerformance Model optionally stores historical data on vendor performance, enabling trend analysis.
    """
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    class Meta:
        db_table = "historical_performance"
