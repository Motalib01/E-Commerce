from django.urls import path
from .views import RegisterView, CustomLoginView
from orders.views import OrderHistoryView 

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),
    path('login/', CustomLoginView.as_view(), name='user-login'),
    
    path('orders/history/', OrderHistoryView.as_view(), name='user-order-history'),
]
