from django.db import models

class Shop(models.Model):
    name = models.CharField("Названия магазин", max_length=255)
    address = models.CharField("Адресс", max_length=255)
    phone = models.CharField("Телефон", max_length=20)
    whatsapp_number = models.CharField("Ватсап Номер", max_length=20)
    description = models.TextField("Краткое описание", blank=True, null=True)
    website = models.URLField("Адресс вашего сайта", blank=True, null=True)
    instagram_link = models.URLField("Instagram ссылка", blank=True, null=True)
    facebook_link = models.URLField("Facebook ссылка", blank=True, null=True)
    start_time = models.TimeField("Начало работы")
    end_time = models.TimeField("Окончание работы")
    personal_courier = models.BooleanField("Личный Курьер", default=False)
    round_the_clock = models.BooleanField("Кругло Суточно", default=False)
    shop_description = models.TextField("Описание Магазин", blank=True, null=True)
    payment_methods = models.CharField("Оплата", max_length=255)
    image = models.ImageField("Фото", upload_to='shop_images/', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"

