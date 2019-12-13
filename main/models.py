from django.db import models


# Create your models here.


class Phone(models.Model):
    name = models.CharField('Назва Телефону', max_length=100)
    about = models.TextField()
    diagonal = models.PositiveSmallIntegerField()
    resolution = models.CharField(max_length=15)
    ram = models.IntegerField()
    rom = models.IntegerField()
    mah = models.IntegerField()
    main_cam = models.PositiveSmallIntegerField()
    front_cam = models.PositiveSmallIntegerField(default=None)
    matrix = models.CharField(max_length=10)
    cpu = models.CharField(max_length=30)
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

    def __str__(self):
        return self.name
