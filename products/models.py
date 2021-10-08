from django.db import models

from users.models import TelegramUserModel


class CategoryModel(models.Model):
    title = models.CharField(max_length=255)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class ProductModel(models.Model):
    title = models.CharField(max_length=255)
    price = models.FloatField()
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='products')
    category = models.ForeignKey(CategoryModel, on_delete=models.PROTECT, related_name='products')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'product'
        verbose_name_plural = 'products'


class OrderModel(models.Model):
    user = models.ForeignKey(TelegramUserModel, related_name='orders', on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductModel, related_name='orders')

    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
