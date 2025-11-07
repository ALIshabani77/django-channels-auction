# auction/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.AuctionItemListView.as_view(), name='auction-list'),
    path('items/<int:item_id>/bid/', views.PlaceBidView.as_view(), name='auction-bid'),
]