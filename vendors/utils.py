from django.db.models import ExpressionWrapper, F, Avg, fields
from django.db.models import DurationField
from django.db.utils import DataError, IntegrityError
from .models import PurchaseOrder, Vendor


def calculate_vendor_performance(vendor_id):
    """
    :param vendor_id:
    :return: Calculated Results Per Vendor.
    Calculations are done depending upon the data and Vendor ID.
    """
    # Ensure vendor_id is an integer
    try:
        vendor_id = int(vendor_id)
    except ValueError:
        return {"error": "Invalid vendor ID. A numerical ID is required."}

    # Get the vendor instance
    try:
        vendor = Vendor.objects.get(id=vendor_id)
    except Vendor.DoesNotExist:
        return {"error": "Vendor not found."}

    # On-Time Delivery Rate
    completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status="completed")
    on_time_deliveries = completed_pos.filter(
        delivery_date__gte=F("order_date")
    ).count()
    total_completed_pos = completed_pos.count()
    on_time_delivery_rate = (
        (on_time_deliveries / total_completed_pos * 100)
        if total_completed_pos > 0
        else 0
    )

    # Quality Rating Average
    quality_ratings = completed_pos.exclude(quality_rating__isnull=True).aggregate(
        Avg("quality_rating")
    )
    quality_rating_avg = quality_ratings["quality_rating__avg"] or 0

    # Average Response Time
    response_times = PurchaseOrder.objects.filter(
        vendor=vendor, acknowledgment_date__isnull=False
    ).annotate(
        response_time=ExpressionWrapper(
            F("acknowledgment_date") - F("issue_date"),
            output_field=fields.DurationField(),
        )
    )
    average_response_time = response_times.aggregate(Avg("response_time"))[
        "response_time__avg"
    ]
    average_response_time_hours = (
        average_response_time.total_seconds() / 3600 if average_response_time else 0
    )

    # Fulfilment Rate
    total_pos = PurchaseOrder.objects.filter(vendor=vendor).count()
    fulfilled_pos = completed_pos.filter(quality_rating__isnull=False).count()
    fulfillment_rate = (fulfilled_pos / total_pos * 100) if total_pos > 0 else 0

    # Update the vendor model
    Vendor.objects.filter(id=vendor_id).update(
        on_time_delivery_rate=on_time_delivery_rate,
        quality_rating_avg=quality_rating_avg,
        average_response_time=average_response_time_hours,
        fulfillment_rate=fulfillment_rate,
    )

    return {
        "on_time_delivery_rate": on_time_delivery_rate,
        "quality_rating_avg": quality_rating_avg,
        "average_response_time": average_response_time_hours,
        "fulfillment_rate": fulfillment_rate,
    }


def recalculate_average_response_time(vendor):
    """
    This function will update acknowledgment_date and trigger the recalculation
    of average_response_time.
    :param purchase_order: ID
    """
    try:
        # Filter purchase orders for the given vendor that have acknowledgment date
        purchase_orders = PurchaseOrder.objects.filter(
            vendor=vendor, acknowledgment_date__isnull=False
        )

        # Efficient Calculation: Use aggregation functions to calculate average response time
        response_times = purchase_orders.annotate(
            response_time=ExpressionWrapper(
                F("acknowledgment_date") - F("issue_date"), output_field=DurationField()
            )
        ).aggregate(avg_response_time=Avg("response_time"))["avg_response_time"]

        # Data Integrity: Ensure response_times is not None before proceeding
        if response_times is not None:
            # Update the average_response_time field of the vendor
            vendor.average_response_time = response_times.total_seconds() / 3600
            vendor.save()
    except (DataError, IntegrityError) as e:
        # Data Integrity: Handle scenarios like missing data points or division by zero
        print(
            f"Error occurred while recalculating average response time for vendor {vendor.name}: {e}"
        )
    except Exception as e:
        # Handle other unexpected errors
        print(f"An unexpected error occurred: {e}")
