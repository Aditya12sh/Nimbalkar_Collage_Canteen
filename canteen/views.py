from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# Home page
def index(request):
    return render(request, "index.html")

# Menu page
def menu(request):
    return render(request, "menu.html")

# Contact page
def contactus(request):
    return render(request,"contactus.html")

# Order page
def order_page(request):
    return render(request, "order.html")

# About page
def about(request):
    return render(request,"about.html")

# Cart page
def cart(request):
    return render(request,"cart.html")

# Logout
def logout_user(request):
    logout(request)
    return redirect("index")

# Login view
def login_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            username = User.objects.get(email=email).username
        except User.DoesNotExist:
            messages.error(request, "Email not registered.")
            return redirect("login")

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Incorrect password.")
            return redirect("login")

    return render(request, "login.html")

# Signup view
def signup_user(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")  # match HTML field
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("signup")

        username = email.split("@")[0]

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
        user.first_name = full_name
        user.save()

        messages.success(request, "Account created successfully! Please login.")
        return redirect("login")

    return render(request, "login_signup.html")

# Login/Signup combined page
def login_signup(request):
    return render(request, "login_signup.html")
