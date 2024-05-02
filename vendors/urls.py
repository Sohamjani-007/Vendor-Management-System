from django.urls import path

from . import views
from .views import VendorView

urlpatterns = [
    # Just a Ping url.
    path("ping/", views.VendorPing.as_view(), name="ping"),
    # POST /api/vendors/ - Create a new vendor
    path("create-vendors/", views.VendorView.as_view(), name="create_vendor"),
    # GET /api/vendors/ - List all vendors
    path("vendors/", VendorView.as_view(), name="list_vendors"),
    # GET /api/vendors/{vendor_id}/ - Retrieve a specific vendor's details
    path("vendors/<int:vendor_id>/", VendorView.as_view(), name="retrieve_vendor"),
    # PUT /api/vendors/{vendor_id}/ - Update a vendor's details
    path("vendors/<int:vendor_id>/", VendorView.as_view(), name="update_vendor"),
    # DELETE /api/vendors/{vendor_id}/ - Delete a vendor
    path("api/vendors/<int:vendor_id>/", VendorView.as_view(), name="delete_vendor"),
    path("vendors/<int:pk>/performance/", views.VendorPerformance.as_view()),
    path("purchase_orders/", views.PurchaseOrderListCreate.as_view()),
    path(
        "purchase_orders/<int:pk>/", views.PurchaseOrderRetrieveUpdateDestroy.as_view()
    ),
    path(
        "purchase_orders/<int:po_id>/acknowledge/",
        views.AcknowledgePurchaseOrder.as_view(),
    ),
]
