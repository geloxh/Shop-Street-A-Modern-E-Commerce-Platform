from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Address

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile.html'

class AddressListView(LoginRequiredMixin, ListView):
    model = Address
    template_name = 'accounts/addresses.html'
    context_object_name = 'addresses'
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

class AddressCreateView(LoginRequiredMixin, CreateView):
    model = Address
    template_name = 'accounts/address_form.html'
    fields = ['title', 'first_name', 'last_name', 'company', 'address_line_1', 
              'address_line_2', 'city', 'state', 'postal_code', 'country', 'phone', 'is_default']
    success_url = reverse_lazy('accounts:addresses')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Address added successfully!')
        return super().form_valid(form)

class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Address
    template_name = 'accounts/address_form.html'
    fields = ['title', 'first_name', 'last_name', 'company', 'address_line_1', 
              'address_line_2', 'city', 'state', 'postal_code', 'country', 'phone', 'is_default']
    success_url = reverse_lazy('accounts:addresses')
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Address updated successfully!')
        return super().form_valid(form)

class AddressDeleteView(LoginRequiredMixin, DeleteView):
    model = Address
    template_name = 'accounts/address_confirm_delete.html'
    success_url = reverse_lazy('accounts:addresses')
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Address deleted successfully!')
        return super().delete(request, *args, **kwargs)