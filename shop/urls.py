from django.urls import path
from . import views

app_name = "shop"
urlpatterns = [
    path('', views.shop, name="shop"),
    path('product/<int:prod_id>', views.product, name='product'),
    path('cart/', views.cart, name="cart")
]
