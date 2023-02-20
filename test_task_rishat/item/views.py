import json

import stripe
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.views import View
from django.views.generic import CreateView, TemplateView, ListView
from requests import Response

from item.forms import ItemForm
from item.models import Item, Order, Discount, Tax

stripe.api_key = settings.SECRET_KEY_STRIPE


class BuyItemView(CreateView):

    def get(self, request, *args, **kwargs):
        id_order = self.kwargs['pk']
        order = Order.objects.get(id=id_order)

        customer = stripe.Customer.create(email='shatilov.demid@gmail.com')

        checkout_session = stripe.PaymentIntent.create(
            amount=order.get_price(),
            currency='usd',
            customer=customer['id'],
            payment_method_types=["card"],
            metadata={
                "order_id": order.id
            },
        )

        return JsonResponse({'clientSecret': checkout_session['client_secret']})
        # return JsonResponse({'id': checkout_session.id})

    # def post(self, request, *args, **kwargs):
    #
    #     ids_list = self.request.POST
    #     x = ids_list
    #     items_list = [Item.objects.get(id=item_id) for item_id in ids_list]
    #     checkout_session = stripe.checkout.Session.create(
    #         payment_method_types=['card'],
    #         mode='payment',
    #         line_items=[
    #             {
    #                 'price_data':
    #                     {
    #                         'currency': 'usd',
    #                         'unit_amount': items_list[0].price,
    #                         'product_data': {
    #                             'name': items_list[0].name
    #                         },
    #                     },
    #                 'tax_rates': [
    #                     {
    #                         'display_name': "VAT",
    #                         'description': "VAT Germany",
    #                         'jurisdiction': "DE",
    #                         'percentage': 16,
    #                         'inclusive': True,
    #                         'active': True
    #                     }
    #                 ],
    #                 'quantity': 1
    #             }
    #         ],
    #         automatic_tax={
    #             'enabled': True
    #         },
    #         metadata={
    #             "item_id": items_list[0].id
    #         },
    #         success_url=settings.DOMAIN + '/success.html',
    #         cancel_url=settings.DOMAIN + '/cancel.html',
    #     )
    #
    #     return JsonResponse({'id': checkout_session.id})


class ItemCardView(TemplateView):
    template_name = 'item_card.html'

    def get_context_data(self, **kwargs):
        id_item = int(self.kwargs['pk'])
        item = Item.objects.get(id=id_item)
        context = super(ItemCardView, self).get_context_data(**kwargs)

        context.update({
            'item': item,
            'PUBLIC_KEY_STRIPE': settings.PUBLIC_KEY_STRIPE,
        })

        return context


class ListItemsView(TemplateView):
    template_name = 'list_items.html'

    def get_context_data(self, **kwargs):

        items_list = Item.objects.all()
        context = super(ListItemsView, self).get_context_data(**kwargs)
        context.update({
            'items_list': items_list,
            'PUBLIC_KEY_STRIPE': settings.PUBLIC_KEY_STRIPE,
        })

        return context


class CreateOrderView(CreateView):
    model = Order
    queryset = Order.objects.all()
    fields = ['items_list', 'tax', 'discount']

    def post(self, request, *args, **kwargs):
        """
        Находим все ID выделенных товаров, узнаем, выбрал ли пользователь налог и скидку, а после создаем Order и
         перенаправляем пользователя на страницу оплаты заказа
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = self.request.POST

        items_id = [int(item_id) for item_id in data if item_id.isdigit()]
        order = Order.objects.create()
        order.items_list.set(items_id)
        if data.get('tax'):
            order.tax = Tax.objects.get(id=1)

        if data.get('discount'):
            order.discount = Discount.objects.get(id=1)

        order.save()

        return redirect('payment_items', order.id)


class PaymentItemsView(TemplateView):
    template_name = 'payment_items.html'

    def get_context_data(self, **kwargs):
        id_order = self.kwargs['pk']
        order = Order.objects.get(id=id_order)
        price = 0
        items_list = order.items_list.all()
        for item in items_list:
            price += item.price

        context = super(PaymentItemsView, self).get_context_data(**kwargs)
        context.update({
            'price': order.get_display_price(),
            'PUBLIC_KEY_STRIPE': settings.PUBLIC_KEY_STRIPE,
            'order_id': id_order
        })

        return context


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"
