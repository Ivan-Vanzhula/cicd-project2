from django.test import TestCase
from online_shop.mvc.models.models import Product, Cart, CartItem

class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Test Product",
            description="This is a test product",
            price=99.99,
            image="products/test.png",
            rating=4,  # Новое поле для рейтинга
            specifications="Test specifications"  # Новое поле для спецификаций
        )

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Test Product")
        self.assertEqual(self.product.description, "This is a test product")
        self.assertEqual(self.product.price, 99.99)
        self.assertEqual(self.product.image, "products/test.png")
        self.assertEqual(self.product.rating, 4)  # Проверка нового поля rating
        self.assertEqual(self.product.specifications, "Test specifications")  # Проверка нового поля specifications

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product")

class CartModelTest(TestCase):
    def setUp(self):
        self.cart = Cart.objects.create(cart_id="test_cart")

    def test_cart_creation(self):
        self.assertEqual(self.cart.cart_id, "test_cart")

    def test_cart_str(self):
        self.assertEqual(str(self.cart), "test_cart")

class CartItemModelTest(TestCase):
    def setUp(self):
        # Создаем продукт для тестирования
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            price=10.0
        )
        # Создаем корзину для тестирования
        self.cart = Cart.objects.create(cart_id="test_cart")

        # Создаем элемент корзины для тестирования
        self.cart_item = CartItem.objects.create(
            product=self.product,
            cart=self.cart,
            quantity=1
        )
    def test_cart_item_creation(self):
        self.assertEqual(self.cart_item.product, self.product)
        self.assertEqual(self.cart_item.cart, self.cart)
        self.assertEqual(self.cart_item.quantity, 1)  # Исправлено на ожидаемое значение 1
        self.assertTrue(self.cart_item.is_active)

    def test_cart_item_sub_total(self):
        self.assertEqual(self.cart_item.sub_total(), self.product.price * self.cart_item.quantity)

    def test_cart_item_str(self):
        # Проверяем, что строковое представление элемента корзины содержит название продукта
        expected_str = self.cart_item.product.name
        self.assertEqual(str(self.cart_item), expected_str)