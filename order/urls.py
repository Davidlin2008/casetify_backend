from django.urls import path 
from .views      import ShopBasketAddView, ShopBasketView, OrderView, OrderCheckoutView

urlpatterns = [
    path('/shopbasketadd', ShopBasketAddView.as_view()),
    path('/shopbasketview', ShopBasketView.as_view()),
    path('/orderview', OrderView.as_view()),
    path('/ordercheckout', OrderCheckoutView.as_view()),
]
