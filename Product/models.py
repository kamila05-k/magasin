from django.db import models
from django.contrib.auth.models import User  # Замените на свою пользовательскую модель, если используете кастомную

class Category(models.Model):
    CATEGORY_CHOICES = [
        ('пылесос', 'Пылесос'),
        ('холодильник', 'Холодильник'),
        ('утюг', 'Утюг'),
        ('морозильник', 'Морозильник'),
        ('телевизор', 'Телевизор'),
        ('аристон', 'Аристон'),
        ('вафельница', 'Вафельница'),
        ('блендер', 'Блендер'),
        ('миксер', 'Миксер'),
        ('вытяжка', 'Вытяжка'),
        ('стиральная_машина', 'Стиральная машина'),
        ('кондиционер', 'Кондиционер'),
    ]

    name = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        unique=True,
        verbose_name="Категория"
    )

    def __str__(self):
        return dict(self.CATEGORY_CHOICES).get(self.name, self.name)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название", blank=False)
    model = models.CharField(max_length=255, verbose_name="Модель", blank=False)
    country = models.CharField(max_length=255, verbose_name="Страна", blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена", blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    image = models.ImageField()
    specifications = models.TextField(verbose_name="Характеристики", blank=True)  # Добавлено поле характеристик
    store_name = models.CharField(max_length=255, verbose_name="Магазин", blank=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
