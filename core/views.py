from django.shortcuts import render, redirect, get_object_or_404

from item.models import Category, Item, CartItem, Cart
from .forms import SignupForm, LoginForm, ProfileForm

from django.contrib.auth import login as auth_login, logout
from django.contrib.auth.decorators import login_required

from .models import UserProfile, Order, OrderItem
from django.db.models import Exists, OuterRef

from django.contrib import messages

# Create your views here.

def index(request):
    items = Item.objects.filter(is_sold=False)[0:6]
    categories = Category.objects.all()

    if request.user.is_authenticated:
        items = items.annotate(
            in_cart=Exists(
                CartItem.objects.filter(
                    cart__user=request.user,
                    cart__is_active=True,
                    item=OuterRef('pk')
                )
            )
        )
    else:
        for item in items:
            item.in_cart = False

    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })
def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('core:index')

    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('core:index')
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('core:index')

@login_required(login_url='/login/')
def myaccount(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('core:myaccount')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'core/myaccount.html', {'form': form})

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user, is_active=True)

    if request.method == 'POST':
        profile = request.user.profile

        order = Order.objects.create(
            user=request.user,
            total_price=cart.total_price,
            shipping_address=profile.address,
            card_last4=profile.card_number[-4:]
        )

        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                item=cart_item.item,
                quantity=cart_item.quantity,
                price=cart_item.item.price
            )

        cart.is_active = False
        cart.save()

        Cart.objects.create(user=request.user)

        messages.success(request, 'Your order has been placed successfully!')
        return redirect('core:order_detail', pk=order.pk)

    return render(request, 'core/checkout.html', {
        'cart': cart,
        'profile': request.user.profile
    })

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    return render(request, 'core/order_detail.html', {'order': order})

@login_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Order has been cancelled successfully.')
    else:
        messages.error(request, 'This order cannot be cancelled.')

    return redirect('core:order_detail', pk=order.pk)

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/order_history.html', {'orders': orders})

def about(request):
    return render(request, 'core/about.html')

def privacy(request):
    return render(request, 'core/privacy.html')

def terms(request):
    return render(request, 'core/terms.html')