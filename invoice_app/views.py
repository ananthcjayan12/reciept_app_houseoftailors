from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Receipt
from .forms import ReceiptForm
from django.db.models import Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import os
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

def list_receipts(request):
    # Get the search query from the GET request
    query = request.GET.get('search')
    # Get the number of receipts per page from the GET request (default to 10)
    per_page = request.GET.get('per_page', 10)

    if query:
        receipts = Receipt.objects.filter(
            Q(name__icontains=query) |
            Q(contact_number__icontains=query) |
            Q(invoice_number__icontains=query) |
            Q(reference_number__icontains=query)
        )
    else:
        receipts = Receipt.objects.all()

    # Set up the paginator
    paginator = Paginator(receipts, per_page)

    # Get the page number from the GET request
    page = request.GET.get('page')

    try:
        receipts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        receipts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page of results
        receipts = paginator.page(paginator.num_pages)

    # Render the response with the paginated receipts
    return render(request, 'list_receipts.html', {'receipts': receipts})



def create_receipt(request):
    if request.method == 'POST':
        form = ReceiptForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_receipts')
    else:
        form = ReceiptForm()
    return render(request, 'create_receipt.html', {'form': form})



def generate_pdf(request, receipt_id):
    # Ensure the model is imported
    from .models import Receipt

    try:
        receipt = Receipt.objects.get(id=receipt_id)
    except Receipt.DoesNotExist:
        return HttpResponse("Receipt not found", status=404)

    html_string = render_to_string('receipt_template.html', {'receipt': receipt})

    html = HTML(string=html_string, base_url=request.build_absolute_uri())
    result = html.write_pdf()

    response = HttpResponse(result, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="receipt_{receipt_id}.pdf"'

    return response

# def generate_pdf(request, id):
#     # Logic for PDF generation
#     pass

