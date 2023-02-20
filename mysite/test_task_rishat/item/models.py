from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.fields import GenericForeignKey


# Create your models here.
class Item(models.Model):

    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100)
    price = models.IntegerField()
    currency = models.CharField(max_length=10)

    def __str__(self):
        return self.name

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)


class Discount(models.Model):

    discount = models.IntegerField()


class Tax(models.Model):

    tax = models.IntegerField()


class Order(models.Model):

    items_list = models.ManyToManyField('Item')
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True)

    def get_price(self):
        """
        Возвращает итоговую цену
        :return:
        """
        price = sum([item.price for item in self.items_list.all()])
        if self.tax is not None:
            price += price * (self.tax.tax / 100)

        if self.discount is not None:
            price -= price * (self.discount.discount / 100)

        return int(price)

    def get_display_price(self):
        """
        Возвращает итоговую цену для клиента
        :return:
        """
        return "{0:.2f}".format(self.get_price() / 100)