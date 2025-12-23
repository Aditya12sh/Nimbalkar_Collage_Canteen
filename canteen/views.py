from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .models import FoodItem, Order, OrderItem


# ================= HOME =================

def index(request):
    return render(request, "index.html")


# ================= AUTH =================
def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        next_url = request.POST.get("next") or request.GET.get("next")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email not registered")
            return redirect("login")

        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        if user:
            login(request, user)

            # ✅ IMPORTANT LOGIC
            if next_url:
                return redirect(next_url)
            else:
                return redirect("menu")

        messages.error(request, "Invalid password")
        return redirect("login")

    return render(request, "login_user.html")


def signup_user(request):
    if request.method == "POST":
        name = request.POST.get("full_name")
        email = request.POST.get("email")
        p1 = request.POST.get("password1")
        p2 = request.POST.get("password2")

        if p1 != p2:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("signup")

        user = User.objects.create_user(
            username=email,
            email=email,
            password=p1
        )
        user.first_name = name
        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")   # ✅ IMPORTANT

    return render(request, "signup_user.html")

def logout_user(request):
    logout(request)
    return redirect("index")


# ================= MENU =================
def menu(request):
    items = FoodItem.objects.all()
    return render(request, 'menu.html', {
        'items': items
    })
# ================= CART (SESSION BASED) =================

def add_to_cart(request, item_id):
    item = get_object_or_404(FoodItem, id=item_id)
    cart = request.session.get("cart", {})

    if str(item_id) in cart:
        cart[str(item_id)]["quantity"] += 1
    else:
        cart[str(item_id)] = {
            "name": item.name,
            "price": item.price,
            "quantity": 1
        }

    request.session["cart"] = cart
    return redirect("cart")


def cart(request):
    cart = request.session.get("cart", {})
    items = []
    total = 0

    for key, value in cart.items():
        subtotal = value["price"] * value["quantity"]
        total += subtotal
        items.append({
            "id": key,
            "name": value["name"],
            "price": value["price"],
            "quantity": value["quantity"],
            "subtotal": subtotal
        })

    return render(request, "cart.html", {
        "items": items,
        "total": total
    })


# ================= CHECKOUT / ORDER =================
@login_required
def place_order(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, "Your cart is empty")
        return redirect('menu')

    # DO NOT create order here
    return redirect('payment')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "order.html", {"orders": orders})


# ================= STATIC =================

def about(request):
    return render(request, "about.html")


def contactus(request):
    return render(request, "contactus.html")

@login_required
def payment(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.error(request, "Your cart is empty")
        return redirect('menu')

    total = 0
    for item in cart.values():
        total += item['price'] * item['quantity']

    return render(request, 'payment.html', {
        'total': total
    })


@login_required
def payment_success(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('menu')

    order = Order.objects.create(
        user=request.user,
        status="Pending Payment Approval"
    )

    for item_id, item in cart.items():
        food = FoodItem.objects.get(id=item_id)
        OrderItem.objects.create(
            order=order,
            item=food,
            quantity=item['quantity']
        )

    request.session['cart'] = {}

    messages.success(request, "Payment successful. Order placed!")
    return redirect('my_orders')
