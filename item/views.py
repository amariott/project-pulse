from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Cart, CartItem, Category
from django.contrib.auth.decorators import login_required

from django.db.models import Q

from .forms import NewItemForm

# Create your views here.

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'item/detail.html', {
      'item': item,
      'related_items': related_items
    })

@login_required
def add_to_cart(request, pk):
    item = get_object_or_404(Item, pk=pk)
    referer = request.META.get('HTTP_REFERER')

    cart, created = Cart.objects.get_or_create(
        user=request.user,
        is_active=True,
        defaults={'user': request.user}
    )

    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart,
        item=item,
        defaults={'quantity': 1}
    )

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect(referer if referer else 'core:index')

@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(
        user=request.user,
        is_active=True
    )
    return render(request, 'item/cart.html', {'cart': cart})

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    in_cart = False
    if request.user.is_authenticated:
        in_cart = CartItem.objects.filter(
            cart__user=request.user,
            cart__is_active=True,
            item=item
        ).exists()

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items,
        'in_cart': in_cart
    })

def browse(request):
    items = Item.objects.filter(is_sold=False)
    categories = Category.objects.all()
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    category_id = request.GET.get('category')
    min_rating = request.GET.get('min_rating')
    query = request.GET.get('query', '')

    if min_price:
        items = items.filter(price__gte=min_price)
    if max_price:
        items = items.filter(price__lte=max_price)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    return render(request, 'item/browse.html', {
        'items': items,
        'categories': categories,
        'query': query,
        'min_price': min_price,
        'max_price': max_price,
        'category_id': int(category_id) if category_id else None,
        'min_rating': min_rating
    })

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            return redirect('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })

@login_required
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user, is_active=True)
    cart_item = get_object_or_404(CartItem, cart=cart, item__id=item_id)
    cart_item.delete()
    return redirect('item:cart')

@login_required
def update_cart_item(request, item_id):
    cart = get_object_or_404(Cart, user=request.user, is_active=True)
    cart_item = get_object_or_404(CartItem, cart=cart, item__id=item_id)

    if request.method == 'POST':
        quantity = request.POST.get('quantity', 1)
        try:
            quantity = int(quantity)
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
        except ValueError:
            pass

    return redirect('item:cart')