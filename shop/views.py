from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect

from wallet.models import Wallet
from .models import Product, Cart, CartItem, Order, OrderItem
from django.http import JsonResponse


# Create your views here.

def shop(request):
    products = Product.objects.all()
    user_cart = Cart.objects.filter(user=request.user)
    cart_item_ids = []
    if user_cart.exists():
        for item in user_cart.first().items.all():
            cart_item_ids.append(item.product_id)
    context = {
        'products': products,
        'cart_item_ids': cart_item_ids
    }
    return render(request, 'shop/shop.html', context)


def product(request, prod_id):
    prod = Product.objects.get(id=prod_id)
    user_cart = Cart.objects.filter(user=request.user)
    cart_item_ids = []
    if user_cart.exists():
        for item in user_cart.first().items.all():
            cart_item_ids.append(item.product_id)
    context = {
        'product': prod,
        'cart_item_ids': cart_item_ids
    }
    return render(request, 'shop/product.html', context)


def cart(request):
    return render(request, 'shop/cart.html')


def add_to_cart(request, prod_id=None):
    # Unpack the tuple returned by get_or_create
    user_cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    if request.method == "POST":
        prod_name = request.POST.get('product_name')
        quantity = request.POST.get('quantity')
        try:
            # Get the product using get_object_or_404 for better error handling
            prod = get_object_or_404(Product, name=prod_name)

            # Create the CartItem
            item, created = CartItem.objects.get_or_create(
                cart=user_cart,
                product=prod,
                quantity=quantity
            )

            item.save()

            # Return success response with cart count
            return JsonResponse({'success': 'Item added to cart.', 'cart_count': user_cart.cart_count})

        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product not found.'})
        except Exception as e:
            # Catch specific errors and send appropriate messages
            return JsonResponse({'error': f"Add to cart failed: {str(e)}"})
    if prod_id:
        prod = get_object_or_404(Product, id=prod_id)
        # Create the CartItem
        item, created = CartItem.objects.get_or_create(
            cart=user_cart,
            product=prod,
        )
        item.save()
        return redirect('shop:shop')

    return JsonResponse({'error': 'Invalid request method.'})


def delete_cart_item(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.delete()
    return redirect('shop:cart')


def checkout(request):
    if request.method == 'POST':
        wallet = Wallet.objects.get(user=request.user)
        user_cart = Cart.objects.get(user=request.user)
        total_price = 0

        order = Order.objects.create(
            user=request.user,
        )
        order.save()

        for item in user_cart.items.all():
            total_price += item.total_price
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity
            )
        payment_method = request.POST.get('payment_method')
        if payment_method == 'current' and wallet.investment_balance >= total_price:
            wallet.investment_balance -= Decimal(total_price)
            wallet.save()
            wallet.add_transaction(
                amount=total_price,
                transaction_type="payment",
                account='Current'
            )
            return redirect('shop:success')
        elif payment_method == 'savings' and wallet.savings_balance >= total_price:
            wallet.savings_balance -= Decimal(total_price)
            wallet.save()
            wallet.add_transaction(
                amount=total_price,
                transaction_type="payment",
                account='Savings'
            )
            return redirect('shop:success')
        elif payment_method == 'stripe':
            pass

    return render(request, 'shop/checkout.html')


def success(request):
    request.user.cart.items.all().delete()
    return render(request, 'shop/success.html')


def failed(request):
    return render(request, 'shop/failed.html')
