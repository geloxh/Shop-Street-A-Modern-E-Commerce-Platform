#!/usr/bin/env python3
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_street.settings')
django.setup()

from django.test import Client
from django.urls import reverse

def test_urls():
    client = Client(HTTP_HOST='127.0.0.1:8000')
    
    urls_to_test = [
        ('/', 'Home'),
        ('/products/', 'Products'),
        ('/cart/', 'Cart'),
        ('/accounts/login/', 'Login'),
    ]
    
    for url, name in urls_to_test:
        try:
            response = client.get(url)
            print(f"{name} ({url}): Status {response.status_code}")
            if response.status_code >= 400:
                print(f"  Error: {response.content[:200]}")
        except Exception as e:
            print(f"{name} ({url}): ERROR - {e}")

if __name__ == '__main__':
    test_urls()