from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import FoodItem, Order, OrderItem, Feedback, Payment


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
            return redirect(next_url if next_url else "menu")

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
            username=email,   # ✅ CONSISTENT
            email=email,
            password=p1
        )
        user.first_name = name
        user.save()

        messages.success(request, "Account created successfully. Please login.")
        return redirect("login")

    return render(request, "signup_user.html")


def logout_user(request):
    logout(request)
    return redirect("index")


# ================= MENU =================
def menu(request):
    items = FoodItem.objects.all()
    return render(request, "menu.html", {"items": items})


# ================= CART =================
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


# ================= CHECKOUT =================
@login_required
def place_order(request):
    if not request.session.get("cart"):
        messages.error(request, "Your cart is empty")
        return redirect("menu")

    return redirect("payment")


@login_required
def payment(request):
    cart = request.session.get("cart", {})
    if not cart:
        return redirect("menu")

    total = sum(item["price"] * item["quantity"] for item in cart.values())
    return render(request, "payment.html", {"total": total})


@login_required
def payment_success(request):
    cart = request.session.get("cart", {})
    if not cart:
        return redirect("menu")

    order = Order.objects.create(
        user=request.user,
        status="Paid"
    )

    total = 0
    for item_id, item in cart.items():
        food = FoodItem.objects.get(id=item_id)
        OrderItem.objects.create(
            order=order,
            item=food,
            quantity=item["quantity"]
        )
        total += item["price"] * item["quantity"]

    # ✅ PAYMENT CREATED ONCE (CORRECT)
    Payment.objects.create(
        order=order,
        amount=total,
        payment_method="Demo Gateway",
        status="Success"
    )

    request.session["cart"] = {}
    messages.success(request, "Payment successful! Order placed.")
    return redirect("my_orders")


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "order.html", {"orders": orders})


# ================= STATIC =================
def about(request):
    return render(request, "about.html")


def contactus(request):
    if request.method == "POST":
        Feedback.objects.create(
            user=request.user if request.user.is_authenticated else None,
            email=request.POST.get("email"),
            subject=request.POST.get("subject", "Feedback"),
            message=request.POST.get("message"),
            food_quality=request.POST.get("food_quality", 5),
            service_speed=request.POST.get("service_speed", 5),
        )

        messages.success(request, "Thank you! Your feedback was submitted.")
        return redirect("contactus")

    return render(request, "contactus.html")
