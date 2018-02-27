from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from cart.cart import Cart
from webshop.models import Product
# Create your views here.


def index(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'index.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

def add_to_cart(request, product_id, quantity):
    product = Product.objects.get(productID=product_id)
    cart = Cart(request)
    cart.add(product, product.price, quantity)

def remove_from_cart(request, product_id):
    product = Product.objects.get(productID=product_id)
    cart = Cart(request)
    cart.remove(product)

def get_cart(request):
    return render(request, 'cart.html', dict(cart=Cart(request)))


