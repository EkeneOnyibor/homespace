import requests

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Order, OrderItem, Product


def home(request):
    products = Product.objects.all()
    featured_products = Product.objects.filter(is_featured=True)
    kitchen_products = Product.objects.filter(category="Kitchen")
    bathroom_products = Product.objects.filter(category="Bathroom")
    bedroom_products = Product.objects.filter(category="Bedroom")
    living_room_products = Product.objects.filter(category="Living Room")

    cart = request.session.get("cart", {})
    if not isinstance(cart, dict):
        cart = {}

    return render(
        request,
        "home.html",
        {
            "products": products,
            "featured_products": featured_products,
            "kitchen_products": kitchen_products,
            "bathroom_products": bathroom_products,
            "bedroom_products": bedroom_products,
            "living_room_products": living_room_products,
            "cart_count": sum(cart.values()),
        },
    )


def kitchen(request):
    products = Product.objects.filter(category="Kitchen")

    cart = request.session.get("cart", {})
    if not isinstance(cart, dict):
        cart = {}

    return render(
        request,
        "rooms/kitchen.html",
        {
            "products": products,
            "cart_count": sum(cart.values()),
        },
    )


def bathroom(request):
    products = Product.objects.filter(category="Bathroom")

    cart = request.session.get("cart", {})
    if not isinstance(cart, dict):
        cart = {}

    return render(
        request,
        "rooms/bathroom.html",
        {
            "products": products,
            "cart_count": sum(cart.values()),
        },
    )


def bedroom(request):
    products = Product.objects.filter(category="Bedroom")

    cart = request.session.get("cart", {})
    if not isinstance(cart, dict):
        cart = {}

    return render(
        request,
        "rooms/bedroom.html",
        {
            "products": products,
            "cart_count": sum(cart.values()),
        },
    )


def living_room(request):
    products = Product.objects.filter(category="Living Room")

    cart = request.session.get("cart", {})
    if not isinstance(cart, dict):
        cart = {}

    return render(
        request,
        "rooms/living_room.html",
        {
            "products": products,
            "cart_count": sum(cart.values()),
        },
    )


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get("cart", {})
    if not isinstance(cart, dict):
        cart = {}

    response = render(
        request,
        "product_detail.html",
        {
            "product": product,
            "cart_count": sum(cart.values()),
        },
    )

    response["Cache-Control"] = "no-store, no-cache, must-revalidate"
    response["Pragma"] = "no-cache"

    return response


def cart(request):
    cart = request.session.get("cart", {})

    if not isinstance(cart, dict):
        cart = {}

    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    total = 0
    cart_items = []

    for product in products:
        quantity = cart.get(str(product.id), 0)
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    return render(
        request,
        "cart.html",
        {
            "cart_items": cart_items,
            "total": total,
            "cart_count": sum(cart.values()),
        },
    )


def add_to_cart(request, product_id):
    cart = request.session.get("cart", {})

    if not isinstance(cart, dict):
        cart = {}

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session["cart"] = cart
    request.session.modified = True

    return JsonResponse(
        {
            "success": True,
            "message": "Item added successfully.",
            "cart_count": sum(cart.values()),
        }
    )


def remove_from_cart(request, product_id):
    cart = request.session.get("cart", {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session["cart"] = cart
    request.session.modified = True

    return redirect("cart")


def get_cart_count(request):
    cart = request.session.get("cart", {})

    if not isinstance(cart, dict):
        cart = {}

    return JsonResponse(
        {
            "cart_count": sum(cart.values())
        }
    )


def update_cart(request, product_id):
    cart = request.session.get("cart", {})

    if not isinstance(cart, dict):
        cart = {}

    product_id = str(product_id)
    quantity = int(request.GET.get("quantity", 1))

    if quantity <= 0:
        if product_id in cart:
            del cart[product_id]
    else:
        cart[product_id] = quantity

    request.session["cart"] = cart
    request.session.modified = True

    return JsonResponse(
        {
            "success": True,
            "cart_count": sum(cart.values()),
            "quantity": quantity,
        }
    )


def get_cart_quantity(request, product_id):
    cart = request.session.get("cart", {})

    if not isinstance(cart, dict):
        cart = {}

    quantity = cart.get(str(product_id), 0)

    return JsonResponse(
        {
            "quantity": quantity
        }
    )

@login_required(login_url="login")
def checkout(request):
    cart = request.session.get("cart", {})

    if not isinstance(cart, dict):
        cart = {}

    # Stop user if cart is empty
    if len(cart) == 0:
        messages.error(
            request,
            "⚠️ Your cart is empty. Please add at least one product before proceeding to checkout.",
        )
        return redirect("cart")

    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)

    total = 0
    cart_items = []

    for product in products:
        quantity = cart.get(str(product.id), 0)
        subtotal = product.price * quantity
        total += subtotal

        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )

    if len(cart_items) == 0:
        messages.error(request, "Your cart is empty.")
        return redirect("cart")

    delivery_fee = 5000
    grand_total = total + delivery_fee

    if request.method == "POST":

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "email": request.POST["email"],
            "amount": int(grand_total * 100),  # Kobo
            "callback_url": request.build_absolute_uri("/verify-payment/"),
        }

        response = requests.post(
            "https://api.paystack.co/transaction/initialize",
            json=payload,
            headers=headers,
        )

        res = response.json()

        if res["status"]:

            request.session["checkout_data"] = {
                "full_name": request.POST["full_name"],
                "email": request.POST["email"],
                "phone": request.POST["phone"],
                "address": request.POST["address"],
            }

            request.session["reference"] = res["data"]["reference"]

            return redirect(res["data"]["authorization_url"])

        messages.error(request, "Unable to initialize payment.")
        return redirect("checkout")

    return render(
        request,
        "checkout.html",
        {
            "cart_items": cart_items,
            "total": total,
            "delivery_fee": delivery_fee,
            "grand_total": grand_total,
        },
    )


def signup(request):
    if request.method == "POST":
        full_name = request.POST["full_name"]
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirm_password = request.POST["confirm_password"]

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("signup")

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=full_name,
        )

        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login")

    return render(request, "signup.html")


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:
            login(request, user)

            messages.success(request, "Login successful!")

            next_url = request.GET.get("next")

            if next_url:
                return redirect(next_url)

            return redirect("home")

        messages.error(request, "Invalid username or password.")

    return render(request, "login.html")


def logout_user(request):
    logout(request)
    return redirect("home")


def order_success(request):
    return render(request, "order_success.html")


@login_required(login_url="login")
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by("-created_at")

    return render(
        request,
        "my_orders.html",
        {
            "orders": orders,
        },
    )


@login_required(login_url="login")
def order_details(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user,
    )

    order_items = OrderItem.objects.filter(order=order)

    return render(
        request,
        "order_details.html",
        {
            "order": order,
            "order_items": order_items,
        },
    )


@login_required(login_url="login")
def verify_payment(request):
    reference = request.GET.get("reference")

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    response = requests.get(
        f"https://api.paystack.co/transaction/verify/{reference}",
        headers=headers,
    )

    res = response.json()

    if res["status"] and res["data"]["status"] == "success":

        checkout_data = request.session.get("checkout_data", {})
        cart = request.session.get("cart", {})

        products = Product.objects.filter(id__in=cart.keys())

        total = 0

        order = Order.objects.create(
            user=request.user,
            full_name=checkout_data["full_name"],
            email=checkout_data["email"],
            phone=checkout_data["phone"],
            address=checkout_data["address"],
            total=0,
        )

        for product in products:
            quantity = cart[str(product.id)]

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price,
            )

            total += product.price * quantity

        order.total = total + 5000
        order.save()

        request.session["cart"] = {}
        request.session.pop("checkout_data", None)
        request.session.pop("reference", None)

        return redirect("order_success")

    messages.error(request, "Payment verification failed.")
    return redirect("checkout")


def smart_planner(request):
    recommended_products = Product.objects.none()
    recommendation_text = ""

    if request.method == "POST":
        room = request.POST.get("room")
        style = request.POST.get("style")
        colour = request.POST.get("colour")
        budget = request.POST.get("budget")

        recommended_products = Product.objects.filter(
            category=room,
            style=style,
            colour=colour,
        )

        if budget == "100-300":
            recommended_products = recommended_products.filter(
                price__gte=100000,
                price__lte=300000,
            )

        elif budget == "300-700":
            recommended_products = recommended_products.filter(
                price__gte=300000,
                price__lte=700000,
            )

        elif budget == "700+":
            recommended_products = recommended_products.filter(
                price__gte=700000,
            )

        recommendation_text = (
            f"We recommend a {style} {colour} "
            f"{room.lower()} because it creates a beautiful, "
            f"comfortable and elegant interior that matches "
            f"your preferences."
        )

    return render(
        request,
        "smart_planner.html",
        {
            "recommended_products": recommended_products,
            "recommendation_text": recommendation_text,
        },
    )