from django.shortcuts import render, redirect
# Create your views here.
from .models import Product, Order
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
def home(request):

    query = request.GET.get('search')

    if query:
        products = Product.objects.filter(name__icontains=query)

    else:
        products = Product.objects.all()

    return render(request, 'home.html', {'products': products})
def product_detail(request, id):
    product = Product.objects.get(id=id)
    return render(request, 'product.html', {'product': product})
def cart(request):

    cart = request.session.get('cart', {})

    products = []
    total = 0

    for item_id, quantity in cart.items():

        # OLD ITEMS HANDLE
        if "-" in item_id:
            product_id, color = item_id.split('-')
        else:
            product_id = item_id
            color = "Default"

        product = Product.objects.get(id=product_id)

        product.color = color
        product.quantity = quantity
        product.total_price = product.price * quantity

        total += product.total_price

        products.append(product)

    return render(request, 'cart.html', {
        'products': products,
        'total': total
    })
def add_to_cart(request, id):
    color = request.GET.get('color')
    cart = request.session.get('cart', {})

    if isinstance(cart, list):
        cart = {}

    id = str(id) + "-" + color
    if id in cart:
        cart[id] += 1
    else:
        cart[id] = 1

    request.session['cart'] = cart

    return redirect('/cart/')
def remove_from_cart(request, id, color):

    cart = request.session.get('cart', {})

    item_key = f"{id}-{color}"

    if item_key in cart:

        if cart[item_key] > 1:
            cart[item_key] -= 1

        else:
            del cart[item_key]

    request.session['cart'] = cart

    return redirect('/cart/')
@login_required
def checkout(request):

    cart = request.session.get('cart', {})

    total = 0

    for item_id, quantity in cart.items():

        product_id, color = item_id.split('-')

        product = Product.objects.get(id=product_id)

        total += product.price * quantity

    if request.method == 'POST':

        name = request.POST['name']
        email = request.POST['email']
        address = request.POST['address']

        Order.objects.create(
            name=name,
            email=email,
            address=address,
            total_price=total
        )

        request.session['cart'] = {}

        return redirect('/success/')

    return render(request, 'checkout.html', {
        'total': total
    })
def success(request):

    return render(request, 'success.html')
def register(request):

    if request.method == 'POST':

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']

        # username automatically email ban jayega
        username = email

        # check user already exists
        if User.objects.filter(username=username).exists():

            messages.error(request, "Account already exists. Please login.")
            return redirect('/login/')

        # create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # direct login after register
        login(request, user)

        messages.success(request, "Account Created Successfully!")

        return redirect('/')

    return render(request, 'register.html')
def user_login(request):
    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
            messages.error(request, "You have no account. Please register first.")
        else:
            messages.error(request, "Invalid Username or Password")

    return render(request, 'login.html')
def user_logout(request):
    logout(request)
    return redirect('/')
    messages.error(request, "Invalid Username or Password")
