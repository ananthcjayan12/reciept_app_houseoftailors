from django.contrib import admin
from .models import Receipt  # Adjust the import path based on your app structure



# Optional: Custom Admin Interface
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('invoice_number', 'name', 'amount', 'contact_number', 'reference_number')
    search_fields = ('invoice_number', 'name', 'reference_number')
    list_filter = ('amount',)

# Register the admin class with the model
admin.site.register(Receipt, ReceiptAdmin)
