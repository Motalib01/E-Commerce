from django.urls import path
from .views import OrderCreateView, AllOrdersAdminView

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('all/', AllOrdersAdminView.as_view(), name='all-orders-admin'),
]
