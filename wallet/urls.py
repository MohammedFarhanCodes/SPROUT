from django.urls import path
from . import views

app_name = 'wallet'
urlpatterns = [
    path('', views.wallet_balance, name="wallet_balance"),
    path('transfer_balance/', views.transfer_balance, name="transfer_balance")

]
