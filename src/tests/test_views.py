# tests/test_views.py
import pytest
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import HttpRequest
from online_shop.mvc.models import Product, Cart, CartItem

@pytest.fixture
def product():
    return Product.objects.create(
        name="Test Product",
        description="Test Description",
        price=99.99,
        image="products/test.jpg"
    )

@pytest.mark.django_db
def test_index_view(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_about_view(client):
    url = reverse('about')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_contact_view(client):
    url = reverse('contact')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_service_view(client):
    url = reverse('service')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_shop_single_view(client, product):
    url = reverse('shop_single', args=[product.id])
    response = client.get(url)
    assert response.status_code == 200
    assert 'product' in response.context
    assert response.context['product'] == product

@pytest.mark.django_db
def test_shop_view(client, product):
    url = reverse('shop')
    response = client.get(url)
    assert response.status_code == 200
    assert 'products' in response.context
    assert len(response.context['products']) == 1
    assert response.context['products'][0] == product

@pytest.mark.django_db
def test_order_view(client):
    url = reverse('order')
    response = client.get(url)
    assert response.status_code == 200
