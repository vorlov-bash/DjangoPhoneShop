from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.postgres.fields import JSONField


# Create your models here.


class Phone(models.Model):
    name = models.CharField('Назва Телефону', max_length=100)
    about = models.TextField('Про телефон')
    diagonal = models.FloatField('Діагональ')
    resolution = models.CharField('Роздільна здатність', max_length=15)
    ram = models.PositiveIntegerField('Оперативна пам\'ять')
    rom = models.PositiveIntegerField('Вбудована пам\'ять')
    mah = models.PositiveIntegerField('Ємність')
    main_cam = models.PositiveSmallIntegerField('Основна камера')
    front_cam = models.PositiveSmallIntegerField('Фронтальна камера', default=None)
    matrix = models.CharField('Тип матриці', max_length=20)
    cpu = models.CharField('Процесор', max_length=30)
    quantity = models.PositiveSmallIntegerField('Кількість')
    price = models.PositiveIntegerField('Ціна')
    image = models.ImageField(upload_to='static/img/')

    def item_name(self):
        return self.name

    item_name.short_description = 'Назва'

    def item_quantity(self):
        return self.quantity

    item_quantity.short_description = 'Кількість'

    def item_price(self):
        return self.price

    item_price.short_description = 'Ціна'

    def image_tag(self):
        return mark_safe(f"""<img src="/{self.image}" width="150" height="200" />""")

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.CharField(max_length=100)
    items = JSONField(default=dict)
    cost = models.IntegerField()

    def __str__(self):
        return f'{self.user} {self.items} {self.cost}'

    def item_name(self):
        return self.user

    item_name.short_description = 'Клієнт'

    def item_items(self):
        return self.items

    item_items.short_description = 'Корзина'

    def item_cost(self):
        return self.cost

    item_cost.short_description = 'Загальна ціна'
