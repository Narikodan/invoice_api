from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Invoice, InvoiceDetail
from .serializers import InvoiceSerializer, InvoiceDetailSerializer

class InvoiceListCreateView(APIView):
    def get(self, request):
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = InvoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            # Deserialize and create associated InvoiceDetail instances
            invoice_details_data = request.data.get('details', [])
            for detail_data in invoice_details_data:
                detail_data['invoice'] = serializer.instance.id
                detail_serializer = InvoiceDetailSerializer(data=detail_data)
                if detail_serializer.is_valid():
                    detail_serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InvoiceRetrieveUpdateDestroyView(APIView):
    def get(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = InvoiceSerializer(invoice, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        invoice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class InvoiceDetailCreateView(APIView):
    def post(self, request, pk):
        try:
            invoice = Invoice.objects.get(pk=pk)
        except Invoice.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        detail_data = request.data.copy()
        detail_data['invoice'] = invoice.id

        serializer = InvoiceDetailSerializer(data=detail_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
