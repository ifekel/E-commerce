from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import *
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart', views.cart, name="cart"), 
    path('checkout', views.checkout, name="checkout"),
    path('logout', LogoutView.as_view(next_page='store'), name="logout"),
    path('contact', views.contact, name="contact"),
    path('login', LoginSection.as_view(), name="login"),
    path('create', ProductCreate.as_view(), name="create"),
    path('update/<str:pk>', ProductUpdate.as_view(), name="update"),
    path('delete/<str:pk>', ProductDelete.as_view(), name="delete"),
    path('deleteOrder/<str:pk>', OrderDelete.as_view(), name="deleteOrder"),
    path('deleteCustomer/<str:pk>', CsutomerDelete.as_view(), name="deleteCustomer"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('product/<str:pk>', ProductDetail.as_view(), name="product"),
    path('product_list', ProductList.as_view(), name="productList"),
    path('customers', ProductCustomer.as_view(), name="customers"),
    path('orders', views.getOrderDetails, name="orders"),
    path('register', RegisterPage.as_view(), name="register"),
]