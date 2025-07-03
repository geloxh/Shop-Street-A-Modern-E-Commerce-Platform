from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='detail'),
    path('add/', views.AddToCartView.as_view(), name='add'),
    path('update/', views.UpdateCartView.as_view(), name='update'),
    path('remove/<int:item_id>/', views.RemoveFromCartView.as_view(), name='remove'),
    path('clear/', views.ClearCartView.as_view(), name='clear'),
    path('wishlist/', views.WishlistView.as_view(), name='wishlist'),
    path('wishlist/add/', views.AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
]