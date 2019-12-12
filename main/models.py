from django.db import models


# Create your models here.


class Costume(models.Model):
    name = models.TextField('Назва Костюму', max_length=100)
    about = models.TextField(max_length=300)
    quantity = models.IntegerField('Кількість')
    price = models.IntegerField('Ціна')
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
