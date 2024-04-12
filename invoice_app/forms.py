from django.forms import ModelForm
from .models import Receipt

class ReceiptForm(ModelForm):
    class Meta:
        model = Receipt
        fields = '__all__'
