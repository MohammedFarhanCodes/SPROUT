from django.urls import path
from . import views

app_name = 'stock'
urlpatterns = [
    path('stock_list/', views.stock_list, name='stock_list'),
    path('stock_chart/<str:symbol>/', views.stock_chart, name='stock_chart'),
    path('user_stocks/', views.user_stocks, name='user_stocks')
]
