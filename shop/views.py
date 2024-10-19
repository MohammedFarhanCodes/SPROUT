from django.shortcuts import render
from .models import Product


# Create your views here.

def shop(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, 'shop/shop.html', context)


def product(request, prod_id):
    prod = Product.objects.get(id=prod_id)
    context = {
        'product': prod
    }
    return render(request, 'shop/product.html', context)


def cart(request):
    return render(request, 'shop/cart.html')
