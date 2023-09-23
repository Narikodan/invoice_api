from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Invoice, InvoiceDetail


class InvoiceAPITestCase(APITestCase):
    def setUp(self):
        self.invoice_data = {
            'date': '2023-09-23',
            'invoice_customer_name': 'Test Customer',
        }
        self.detail_data = {
            'description': 'Test Description',
            'quantity': 5,
            'unit_price': '10.00',
            'price': '50.00',
        }

    def test_create_invoice(self):
        url = reverse('invoice-list-create')  # Use the reverse function to get the URL
        response = self.client.post(url, self.invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(Invoice.objects.get().invoice_customer_name, 'Test Customer')

    def test_create_invoice_with_details(self):
        url = reverse('invoice-list-create')  # Use the reverse function to get the URL
        response = self.client.post(url, self.invoice_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        invoice_id = response.data['id']

        # Add details to the created invoice
        detail_url = reverse('invoice-detail-create', args=[invoice_id])  # Get the detail URL
        detail_data = {**self.detail_data, 'invoice': invoice_id}
        response = self.client.post(detail_url, detail_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InvoiceDetail.objects.count(), 1)

    def test_get_invoices(self):
        # Create a test invoice
        Invoice.objects.create(date='2023-09-23', invoice_customer_name='Test Customer')

        url = reverse('invoice-list-create')  # Use the reverse function to get the URL
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_single_invoice(self):
        # Create a test invoice
        invoice = Invoice.objects.create(date='2023-09-23', invoice_customer_name='Test Customer')

        url = reverse('invoice-detail', args=[invoice.id])  # Use reverse to get the detail URL
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['invoice_customer_name'], 'Test Customer')

    def test_update_invoice(self):
        # Create a test invoice
        invoice = Invoice.objects.create(date='2023-09-23', invoice_customer_name='Test Customer')

        updated_data = {
            'date': '2023-09-24',
            'invoice_customer_name': 'Updated Customer',
        }

        url = reverse('invoice-detail', args=[invoice.id])  # Use reverse to get the detail URL
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Invoice.objects.get(id=invoice.id).invoice_customer_name, 'Updated Customer')

    def test_delete_invoice(self):
        # Create a test invoice
        invoice = Invoice.objects.create(date='2023-09-23', invoice_customer_name='Test Customer')

        url = reverse('invoice-detail', args=[invoice.id])  # Use reverse to get the detail URL
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Invoice.objects.count(), 0)
