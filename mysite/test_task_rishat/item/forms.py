from django import forms

from item.models import Item, Order


class ItemForm(forms.ModelForm):

    class Meta():
        model = Item
        exclude = ()