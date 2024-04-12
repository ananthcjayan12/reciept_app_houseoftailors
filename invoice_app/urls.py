from django.urls import path
from .views import list_receipts, create_receipt, generate_pdf

urlpatterns = [
    path('', list_receipts, name='list_receipts'),
    path('create/', create_receipt, name='create_receipt'),
    path('receipts/<int:receipt_id>/pdf/', generate_pdf, name='generate_pdf'),

]
