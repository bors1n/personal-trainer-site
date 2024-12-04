from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('create/', views.create_payment, name='create'),
    path('webhook/', views.payment_webhook, name='webhook'),
    path('complete/', views.payment_complete, name='complete'),
]
