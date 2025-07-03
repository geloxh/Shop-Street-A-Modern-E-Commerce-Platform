// Main JavaScript file for Shop Street

// Utility functions
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Notification system
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 animate-slide-up`;
    
    switch(type) {
        case 'success':
            notification.className += ' bg-green-500 text-white';
            break;
        case 'error':
            notification.className += ' bg-red-500 text-white';
            break;
        case 'warning':
            notification.className += ' bg-yellow-500 text-white';
            break;
        default:
            notification.className += ' bg-blue-500 text-white';
    }
    
    notification.innerHTML = `
        <div class="flex items-center justify-between">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-4 text-white hover:text-gray-200">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, duration);
}

// Cart functionality
class Cart {
    static add(productId, quantity = 1, variantId = null) {
        const formData = new FormData();
        formData.append('product_id', productId);
        formData.append('quantity', quantity);
        if (variantId) {
            formData.append('variant_id', variantId);
        }
        
        return fetch('/cart/add/', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message, 'success');
                this.updateCartCount(data.cart_items_count);
            } else {
                showNotification('Error adding product to cart', 'error');
            }
            return data;
        })
        .catch(error => {
            showNotification('Error adding product to cart', 'error');
            throw error;
        });
    }
    
    static update(itemId, quantity) {
        const formData = new FormData();
        formData.append('item_id', itemId);
        formData.append('quantity', quantity);
        
        return fetch('/cart/update/', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.updateCartCount(data.cart_items_count);
                this.updateCartTotal(data.cart_total);
            }
            return data;
        });
    }
    
    static updateCartCount(count) {
        const cartBadge = document.querySelector('.fa-shopping-cart + span');
        if (cartBadge) {
            cartBadge.textContent = count;
            cartBadge.style.display = count > 0 ? 'flex' : 'none';
        }
    }
    
    static updateCartTotal(total) {
        const totalElements = document.querySelectorAll('.cart-total');
        totalElements.forEach(element => {
            element.textContent = `$${total}`;
        });
    }
}

// Wishlist functionality
class Wishlist {
    static add(productId) {
        const formData = new FormData();
        formData.append('product_id', productId);
        
        return fetch('/cart/wishlist/add/', {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showNotification(data.message, 'success');
            }
            return data;
        })
        .catch(error => {
            showNotification('Error adding to wishlist', 'error');
            throw error;
        });
    }
}

// Image gallery functionality
class ImageGallery {
    constructor(container) {
        this.container = container;
        this.mainImage = container.querySelector('.main-image');
        this.thumbnails = container.querySelectorAll('.thumbnail');
        this.init();
    }
    
    init() {
        this.thumbnails.forEach(thumbnail => {
            thumbnail.addEventListener('click', (e) => {
                e.preventDefault();
                this.setMainImage(thumbnail.src, thumbnail.alt);
                this.setActiveThumbnail(thumbnail);
            });
        });
    }
    
    setMainImage(src, alt) {
        this.mainImage.src = src;
        this.mainImage.alt = alt;
    }
    
    setActiveThumbnail(activeThumbnail) {
        this.thumbnails.forEach(thumb => thumb.classList.remove('active'));
        activeThumbnail.classList.add('active');
    }
}

// Product quantity selector
class QuantitySelector {
    constructor(container) {
        this.container = container;
        this.input = container.querySelector('input[type="number"]');
        this.decreaseBtn = container.querySelector('.decrease');
        this.increaseBtn = container.querySelector('.increase');
        this.init();
    }
    
    init() {
        this.decreaseBtn?.addEventListener('click', () => this.decrease());
        this.increaseBtn?.addEventListener('click', () => this.increase());
    }
    
    decrease() {
        const currentValue = parseInt(this.input.value);
        if (currentValue > 1) {
            this.input.value = currentValue - 1;
            this.input.dispatchEvent(new Event('change'));
        }
    }
    
    increase() {
        const currentValue = parseInt(this.input.value);
        const maxValue = parseInt(this.input.max) || Infinity;
        if (currentValue < maxValue) {
            this.input.value = currentValue + 1;
            this.input.dispatchEvent(new Event('change'));
        }
    }
}

// Initialize components when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize image galleries
    document.querySelectorAll('.image-gallery').forEach(gallery => {
        new ImageGallery(gallery);
    });
    
    // Initialize quantity selectors
    document.querySelectorAll('.quantity-selector').forEach(selector => {
        new QuantitySelector(selector);
    });
    
    // Add to cart buttons
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            const variantId = this.dataset.variantId;
            const quantityInput = this.closest('form')?.querySelector('input[name="quantity"]');
            const quantity = quantityInput ? parseInt(quantityInput.value) : 1;
            
            Cart.add(productId, quantity, variantId);
        });
    });
    
    // Add to wishlist buttons
    document.querySelectorAll('.add-to-wishlist').forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const productId = this.dataset.productId;
            Wishlist.add(productId);
        });
    });
    
    // Cart quantity updates
    document.querySelectorAll('.cart-quantity-input').forEach(input => {
        input.addEventListener('change', function() {
            const itemId = this.dataset.itemId;
            const quantity = parseInt(this.value);
            Cart.update(itemId, quantity);
        });
    });
    
    // Mobile menu toggle
    const mobileMenuButton = document.querySelector('.mobile-menu-button');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Search functionality
    const searchForm = document.querySelector('form[action*="search"]');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchInput = this.querySelector('input[name="q"]');
            if (!searchInput.value.trim()) {
                e.preventDefault();
                showNotification('Please enter a search term', 'warning');
            }
        });
    }
    
    // Auto-hide alerts
    setTimeout(() => {
        document.querySelectorAll('.alert').forEach(alert => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        });
    }, 5000);
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Lazy loading for images
if ('IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    document.querySelectorAll('img[data-src]').forEach(img => {
        imageObserver.observe(img);
    });
}