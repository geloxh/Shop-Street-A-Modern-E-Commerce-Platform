from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.ProfileView.as_view(), name='profile'),
    path('addresses/', views.AddressListView.as_view(), name='addresses'),
    path('addresses/add/', views.AddressCreateView.as_view(), name='add_address'),
    path('addresses/<int:pk>/edit/', views.AddressUpdateView.as_view(), name='edit_address'),
    path('addresses/<int:pk>/delete/', views.AddressDeleteView.as_view(), name='delete_address'),
]