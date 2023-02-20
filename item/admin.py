from django.contrib import admin

from .models import Item, Order
from .forms import ItemForm


# Register your models here.
class ItemAdmin(admin.ModelAdmin):
    form = ItemForm
    model = Item
    list_display = ['id', 'name', 'description', 'currency', 'price']


admin.site.register(Item, ItemAdmin)