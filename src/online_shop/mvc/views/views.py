# mvc/views/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist
from ..models import Product, Cart, CartItem
from django.http import HttpResponse
def index(request):
    return render(request, 'index/index.html')
def about(request):
    return render(request, 'about/about.html')
def contact(request):
    return render(request, 'contact/contact.html')
def service(request):
    return render(request, 'service/service.html')

def shop_single(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product,  # Correcting the variable name here
    }
    return render(request, 'shop_single/shop_single.html', context)

def shop(request):
   # `products = Product.objects.all()` retrieves all instances of the `Product` model from the
   # database.
    query = request.GET.get('query', '')  # Отримання пошукового запиту з GET-параметра
    if query:
        products = Product.objects.filter(name__icontains=query)  # Фільтрує товари за назвою
    else:
        products = Product.objects.all()  # Повертає всі товари, якщо пошуковий запит відсутній
    context = {
        'products': products,
    }
    return render(request, 'shop/shop.html', context)

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()
    try:
        cart_item = CartItem.objects.get(product = product,cart = cart)
        cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product = product, quantity = 1, cart = cart,)
        cart_item.save()
    return redirect('cart')


def remove_cart(request, product_id):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = None
    
    if cart:
        product = get_object_or_404(Product, id=product_id)
        try:
            cart_item = CartItem.objects.get(product=product, cart=cart)
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
        except CartItem.DoesNotExist:
            pass
    
    return redirect('cart')

def remove_item_cart(request,product_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product,id = product_id)
    cart_item = CartItem.objects.get(product = product,cart = cart)
    cart_item.delete()
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax' : tax,
        'grand_total': grand_total
    }
    return render(request, 'cart/cart.html', context)

def order(request):
    return render(request, 'order/order.html')
