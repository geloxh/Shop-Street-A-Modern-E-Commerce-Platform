from django.shortcuts import render
from django.views.generic import TemplateView
from django.db.models import Q
from products.models import Product, Category

class HomeView(TemplateView):
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_products'] = Product.objects.filter(is_featured=True, is_active=True)[:8]
        context['categories'] = Category.objects.filter(is_active=True)[:6]
        context['latest_products'] = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
        return context

class AboutView(TemplateView):
    template_name = 'core/about.html'

class ContactView(TemplateView):
    template_name = 'core/contact.html'

class SearchView(TemplateView):
    template_name = 'core/search.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '')
        
        if query:
            products = Product.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(category__name__icontains=query),
                is_active=True
            ).distinct()
        else:
            products = Product.objects.none()
        
        context['products'] = products
        context['query'] = query
        context['total_results'] = products.count()
        return context