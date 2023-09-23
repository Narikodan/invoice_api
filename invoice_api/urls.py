from django.contrib import admin
from django.urls import path
from api.views import InvoiceDetailCreateView, InvoiceListCreateView, InvoiceRetrieveUpdateDestroyView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('invoices/', InvoiceListCreateView.as_view(), name='invoice-list-create'),
    path('invoices/<int:pk>/', InvoiceRetrieveUpdateDestroyView.as_view(), name='invoice-detail'),
    path('invoices/<int:pk>/details/', InvoiceDetailCreateView.as_view(), name='invoice-detail-create'),
]
