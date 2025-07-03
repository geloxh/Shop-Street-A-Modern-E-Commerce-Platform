#!/usr/bin/env python3
"""
Create sample data for Shop Street E-commerce Platform
This script creates sample categories, products, and other data for testing.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shop_street.settings')
django.setup()

from products.models import Category, Product, ProductImage
from orders.models import Coupon
from django.utils import timezone
from datetime import timedelta

def create_categories():
    """Create sample categories."""
    categories_data = [
        {
            'name': 'Electronics',
            'description': 'Latest electronic gadgets and devices'
        },
        {
            'name': 'Clothing',
            'description': 'Fashion and apparel for all occasions'
        },
        {
            'name': 'Home & Garden',
            'description': 'Everything for your home and garden'
        },
        {
            'name': 'Sports & Outdoors',
            'description': 'Sports equipment and outdoor gear'
        },
        {
            'name': 'Books',
            'description': 'Books, magazines, and educational materials'
        },
        {
            'name': 'Health & Beauty',
            'description': 'Health, beauty, and personal care products'
        }
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
                'is_active': True
            }
        )
        categories.append(category)
        if created:
            print(f"Created category: {category.name}")
    
    return categories

def create_products(categories):
    """Create sample products."""
    products_data = [
        # Electronics
        {
            'name': 'Wireless Bluetooth Headphones',
            'description': 'High-quality wireless headphones with noise cancellation and long battery life.',
            'short_description': 'Premium wireless headphones with excellent sound quality.',
            'category': 'Electronics',
            'price': 99.99,
            'compare_price': 129.99,
            'sku': 'WBH-001',
            'stock_quantity': 50,
            'is_featured': True
        },
        {
            'name': 'Smartphone Case',
            'description': 'Durable protective case for smartphones with shock absorption.',
            'short_description': 'Protective smartphone case with premium materials.',
            'category': 'Electronics',
            'price': 24.99,
            'sku': 'SPC-001',
            'stock_quantity': 100
        },
        {
            'name': '4K Webcam',
            'description': 'Ultra HD webcam perfect for streaming and video calls.',
            'short_description': '4K resolution webcam with auto-focus.',
            'category': 'Electronics',
            'price': 79.99,
            'compare_price': 99.99,
            'sku': 'WC4K-001',
            'stock_quantity': 25,
            'is_featured': True
        },
        
        # Clothing
        {
            'name': 'Cotton T-Shirt',
            'description': 'Comfortable 100% cotton t-shirt available in multiple colors.',
            'short_description': 'Classic cotton t-shirt for everyday wear.',
            'category': 'Clothing',
            'price': 19.99,
            'sku': 'CT-001',
            'stock_quantity': 200
        },
        {
            'name': 'Denim Jeans',
            'description': 'Classic fit denim jeans made from premium denim fabric.',
            'short_description': 'Comfortable and stylish denim jeans.',
            'category': 'Clothing',
            'price': 59.99,
            'compare_price': 79.99,
            'sku': 'DJ-001',
            'stock_quantity': 75,
            'is_featured': True
        },
        
        # Home & Garden
        {
            'name': 'LED Desk Lamp',
            'description': 'Adjustable LED desk lamp with multiple brightness levels and USB charging port.',
            'short_description': 'Modern LED desk lamp with USB charging.',
            'category': 'Home & Garden',
            'price': 39.99,
            'sku': 'LDL-001',
            'stock_quantity': 60
        },
        {
            'name': 'Indoor Plant Pot',
            'description': 'Ceramic plant pot perfect for indoor plants and herbs.',
            'short_description': 'Stylish ceramic pot for indoor plants.',
            'category': 'Home & Garden',
            'price': 14.99,
            'sku': 'IPP-001',
            'stock_quantity': 120
        },
        
        # Sports & Outdoors
        {
            'name': 'Yoga Mat',
            'description': 'Non-slip yoga mat made from eco-friendly materials.',
            'short_description': 'Premium eco-friendly yoga mat.',
            'category': 'Sports & Outdoors',
            'price': 29.99,
            'sku': 'YM-001',
            'stock_quantity': 80,
            'is_featured': True
        },
        
        # Books
        {
            'name': 'Programming Guide',
            'description': 'Comprehensive guide to modern programming languages and techniques.',
            'short_description': 'Essential programming guide for developers.',
            'category': 'Books',
            'price': 34.99,
            'sku': 'PG-001',
            'stock_quantity': 40
        },
        
        # Health & Beauty
        {
            'name': 'Organic Face Cream',
            'description': 'Natural organic face cream with anti-aging properties.',
            'short_description': 'Organic anti-aging face cream.',
            'category': 'Health & Beauty',
            'price': 49.99,
            'compare_price': 64.99,
            'sku': 'OFC-001',
            'stock_quantity': 30
        }
    ]
    
    category_dict = {cat.name: cat for cat in categories}
    
    for prod_data in products_data:
        category = category_dict.get(prod_data['category'])
        if not category:
            continue
            
        product, created = Product.objects.get_or_create(
            sku=prod_data['sku'],
            defaults={
                'name': prod_data['name'],
                'description': prod_data['description'],
                'short_description': prod_data['short_description'],
                'category': category,
                'price': prod_data['price'],
                'compare_price': prod_data.get('compare_price'),
                'stock_quantity': prod_data['stock_quantity'],
                'is_active': True,
                'is_featured': prod_data.get('is_featured', False)
            }
        )
        
        if created:
            print(f"Created product: {product.name}")

def create_coupons():
    """Create sample coupons."""
    coupons_data = [
        {
            'code': 'WELCOME10',
            'discount_type': 'percentage',
            'discount_value': 10,
            'minimum_amount': 50,
            'usage_limit': 100,
            'valid_from': timezone.now(),
            'valid_until': timezone.now() + timedelta(days=30)
        },
        {
            'code': 'SAVE20',
            'discount_type': 'fixed',
            'discount_value': 20,
            'minimum_amount': 100,
            'usage_limit': 50,
            'valid_from': timezone.now(),
            'valid_until': timezone.now() + timedelta(days=15)
        }
    ]
    
    for coupon_data in coupons_data:
        coupon, created = Coupon.objects.get_or_create(
            code=coupon_data['code'],
            defaults=coupon_data
        )
        
        if created:
            print(f"Created coupon: {coupon.code}")

def main():
    """Main function to create all sample data."""
    print("Creating sample data for Shop Street...")
    print("=" * 50)
    
    # Create categories
    print("\nCreating categories...")
    categories = create_categories()
    
    # Create products
    print("\nCreating products...")
    create_products(categories)
    
    # Create coupons
    print("\nCreating coupons...")
    create_coupons()
    
    print("\n" + "=" * 50)
    print("Sample data created successfully!")
    print("\nSummary:")
    print(f"- Categories: {Category.objects.count()}")
    print(f"- Products: {Product.objects.count()}")
    print(f"- Coupons: {Coupon.objects.count()}")
    print("\nYour Shop Street e-commerce platform is ready!")

if __name__ == '__main__':
    main()