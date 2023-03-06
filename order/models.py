from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, DecimalValidator
from django.utils import timezone


class Stock(models.Model):
    name = models.CharField(
        'Название склада',
        max_length=50
    )
    address = models.CharField(
        'Адрес склада',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'Контактный телефон склада',
        max_length=50,
        blank=True,
    )
    common_limit = models.PositiveIntegerField('Общий лимит на хранение товара')

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            StockItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'Название',
        max_length=50
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'Название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='Категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    description = models.TextField(
        'Описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name


class StockItem(models.Model):
    stock = models.ForeignKey(
        Stock,
        related_name='stock_items',
        verbose_name="Склад",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='stock_items',
        verbose_name='Продукт',
    )
    availability = models.BooleanField(
        'Доступные для хранения',
        default=True,
        db_index=True
    )
    price = models.DecimalField(
        'Цена за хранение',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0), DecimalValidator(8, 2)],
    )
    limit = models.PositiveIntegerField('Лимит на хранение товара')

    class Meta:
        verbose_name = 'Товар доступный для хранения на складе'
        verbose_name_plural = 'Товары доступные для хранения на складе'
        unique_together = [
            ['stock', 'product']
        ]

    def __str__(self):
        return f"{self.stock.name} - {self.product.name}"


class Order(models.Model):
    first_name = models.CharField(
        'Имя клиента',
        max_length=50,
        db_index=True,
    )
    last_name = models.CharField(
        'Фамилия клиента',
        max_length=50,
        blank=True,
        db_index=True,
    )
    phonenumber = PhoneNumberField(
        'Номер владельца',
        db_index=True,
    )
    email = models.EmailField('Электронная почта')
    address = models.CharField(
        'Адрес',
        max_length=50,
        blank=True,
        db_index=True,
    )
    created = models.DateTimeField(
        'Время создания',
        null=True,
        db_index=True,
        default=timezone.now,
    )
    updated = models.DateTimeField(
        'Время обновления',
        null=True,
        blank=True,
        db_index=True,
        auto_now=True
    )
    paid = models.BooleanField('Оплачен', default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        verbose_name='Заказ',
        related_name='items',
        null=True,
    )
    product = models.ForeignKey(
        Product,
        verbose_name='Продукт',
        related_name='order_items',
        on_delete=models.SET_NULL,
        null=True,
    )
    price = models.DecimalField(
        'Цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0), DecimalValidator(8, 2)],
    )
    quantity = models.PositiveIntegerField('Количество', null=True)

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f'{self.id}'

    def get_cost(self):
        return self.price * self.quantity

