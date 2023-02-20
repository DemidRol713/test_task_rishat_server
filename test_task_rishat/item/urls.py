from django.urls import path
from item.views import (
    BuyItemView,
    SuccessView,
    CancelView,
    ItemCardView,
    ListItemsView, PaymentItemsView, CreateOrderView
)


urlpatterns = [
    path('item/<pk>', ItemCardView.as_view(), name='item'),
    path('buy/<pk>', BuyItemView.as_view(), name='buy'),
    path('payment_items/<pk>', PaymentItemsView.as_view(), name='payment_items'),
    path('create_order/', CreateOrderView.as_view(), name='create_order'),
    path('', ListItemsView.as_view(), name='list_item'),

    # path('item_catalog/')
]