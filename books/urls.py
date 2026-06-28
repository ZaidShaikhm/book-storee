# books/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('',                          views.index,           name='index'),
    path('api/health/',               views.health,          name='health'),
    path('api/stats/',                views.stats,           name='stats'),
    path('api/books/',                views.books_list,      name='books-list'),
    path('api/books/<str:pk>/',       views.book_detail,     name='book-detail'),
    path('api/customers/',            views.customers_list,  name='customers-list'),
    path('api/customers/<str:pk>/',   views.customer_detail, name='customer-detail'),
    path('api/orders/',               views.orders_list,     name='orders-list'),
    path('api/orders/<str:pk>/',      views.order_detail,    name='order-detail'),
]
