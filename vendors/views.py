from django.views.generic import ListView
from .models import Vendor

class VendorListView(ListView):
    model = Vendor
    template_name = 'vendors/list.html'
    context_object_name = 'vendors'
    
    def get_queryset(self):
        return Vendor.objects.filter(is_active=True)