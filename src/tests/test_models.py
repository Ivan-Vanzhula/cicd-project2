import pytest
from online_shop.mvc.models import *

@pytest.mark.django_db
def test_product_create():
    product = Product.objects.create(
        name="Test Product",
        description="Test Description",
        price=99.99,
        rating=5,
        specifications="Test Specifications"
    )
    assert product.name == "Test Product"
    assert product.description == "Test Description"
    assert product.price == 99.99
    assert product.rating == 5
    assert product.specifications == "Test Specifications"

@pytest.mark.django_db
def test_cart_creation():
    cart = Cart.objects.create(cart_id="test_cart")
    assert cart.cart_id == "test_cart"

@pytest.mark.django_db
def test_cart_item_creation():
    product = Product.objects.create(
        name="Test Product",
        description="Test Description",
        price=99.99,
        rating=5,
        specifications="Test Specifications"
    )
    cart = Cart.objects.create(cart_id="test_cart")
    cart_item = CartItem.objects.create(
        product=product,
        cart=cart,
        quantity=2,
        is_active=True
    )
    assert cart_item.product == product
    assert cart_item.cart == cart
    assert cart_item.quantity == 2
    assert cart_item.is_active == True
    assert cart_item.sub_total() == 199.98