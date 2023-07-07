from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *
from django.http import JsonResponse
from django.http import HttpResponse
import json
import datetime
from .utils import cookieCart, cartData, guestOrder
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy, reverse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import *
from django.contrib.auth.decorators import login_required


# Create your views here.
def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        # Send an email
        send_mail(
            name,  # subject
            message,  # message
            email,  # from email
            ['ifeanyionyekwelu786@gmail.com'],  # To email
        )
        return render(request, 'store/contact.html', {'name': name})
    return render(request, 'store/contact.html')


def success(request, uid):
    template = render_to_string('store/email_template.html', {'name': request.user.email})

    email = EmailMessage(
        'subject',
        template,
        [request.user.email],
    )

    email.fail_silently = False
    email.send()


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action: ', action)
    print('productId: ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete!', safe=False)


# def productDetails(request, item):
#     products = Product.objects.get(id=item)

#     context = {'products': products}
#     return render(request, "store/product_details.html", context)


class LoginSection(LoginView):
    template_name = 'store/login.html'
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('orders')


class ProductDetail(DetailView):
    model = Product
    context_object_name = 'product'
    template_name = 'store/product_details.html'


class ProductCreate(LoginRequiredMixin, CreateView):
    model = Product
    fields = ['name', 'Label','price', 'image']
    success_url = reverse_lazy("productList")
    template_name = 'store/product-create.html'

class ProductUpdate(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'Label','price', 'image']
    success_url = reverse_lazy("productList")
    template_name = 'store/update.html'


class ProductDelete(LoginRequiredMixin, DeleteView):
    model = Product
    context_object_name = 'product'
    success_url = reverse_lazy("productList")
    template_name = 'store/product-delete.html'


class OrderDelete(LoginRequiredMixin, DeleteView):
    model = Order
    context_object_name = 'order'
    success_url = reverse_lazy("orders")
    template_name = 'store/product-delete.html'

class CsutomerDelete(LoginRequiredMixin, DeleteView):
    model = Customer
    context_object_name = 'customer'
    success_url = reverse_lazy("customers")
    template_name = 'store/product-delete.html'


class ProductList(LoginRequiredMixin, ListView):
    model = Product
    context_object_name = 'product'
    template_name = 'store/product-list.html'


class ProductCustomer(LoginRequiredMixin, ListView):
    model = Customer
    context_object_name = 'customers'
    template_name = 'store/customer.html'


@login_required(login_url='login')
def getOrderDetails(request):
    if request.user.is_authenticated:
        order = Order.objects.all()
        orderItems = OrderItem.objects.all()
        shipping = ShippingAddress.objects.all()

        context = {'order': order, 'shipping': shipping, 'orderItems': orderItems}
        return render(request, 'store/orders.html', context)
    else:
        reverse('login')
        return render(request, 'store/err.html')


class RegisterPage(FormView):
    template_name = 'store/signup.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('store')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
