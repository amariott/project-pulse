from django.urls import path
from . import views
app_name = 'item'

urlpatterns = [
    path('<int:pk>/', views.detail, name='detail'),
    path('cart/', views.view_cart, name='cart'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('browse/', views.browse, name='browse'),
    path('new/', views.new, name='new'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
]
