from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Product, Order, OrderItem, GuestCart
from .forms import GuestCheckoutForm

def home(request):
    return render(request, 'store/home.html')


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, 'Account created successfully!')
        return redirect('home')
    return render(request, 'store/signup.html')


# Add to Cart Function
def add_to_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity', 1))  # Default to 1 if quantity is not provided
        customization = request.POST.get('customization', '')

        cart = request.session.get('cart', [])

        # Check if the product already exists in the cart
        product_exists = False
        for item in cart:
            if item['product_id'] == product_id:
                item['quantity'] += quantity  # Increase quantity if the product already exists in cart
                product_exists = True
                break

        if not product_exists:
            cart.append({
                'product_id': product_id,
                'quantity': quantity,
                'customization': customization,
            })

        request.session['cart'] = cart
        request.session.modified = True

        return redirect('cart')  # Redirect to the cart page
def cart_view(request):
    cart = request.session.get('cart', [])
    cart_items = []
    total_price = 0

    for item in cart:
        try:
            product = Product.objects.get(id=item['product_id'])
            quantity = item.get('quantity', 1)
            customization = item.get('customization', '')
            subtotal = product.price * quantity
            total_price += subtotal

            cart_items.append({
                'product': product,
                'quantity': quantity,
                'customization': customization,
                'subtotal': subtotal
            })
        except Product.DoesNotExist:
            continue

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })



def remove_from_cart(request, index):
    cart = request.session.get('cart', [])
    try:
        # Removing one quantity or the item entirely if quantity reaches 0
        cart_item = cart[index]
        if cart_item['quantity'] > 1:
            cart_item['quantity'] -= 1  # Decrease quantity by 1
        else:
            cart.pop(index)  # Remove item from cart if quantity is 1
        request.session['cart'] = cart
    except IndexError:
        pass
    request.session.modified = True
    return redirect('cart')

def checkout_view(request):
    cart = request.session.get('cart', [])
    cart_items = []
    total_price = 0

    for item in cart:
        try:
            product = Product.objects.get(id=item['product_id'])
            quantity = item.get('quantity', 1)
            customization = item.get('customization', '')
            subtotal = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'customization': customization,
                'subtotal': subtotal,
            })
            total_price += subtotal
        except Product.DoesNotExist:
            continue

    if request.method == 'POST':
        form = GuestCheckoutForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            order = Order.objects.create(guest_name=name, guest_email=email)

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    customization=item['customization']
                )

            request.session['cart'] = []
            request.session.modified = True
            return render(request, 'store/thankyou.html', {'order': order})
    else:
        form = GuestCheckoutForm()

    return render(request, 'store/checkout.html', {
        'form': form,
        'cart_items': cart_items,
        'total_price': total_price
    })


def save_guest_cart(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        cart = request.session.get('cart', [])
        
        GuestCart.objects.create(
            name=name,
            email=email,
            cart_data=cart
        )
        messages.success(request, 'Cart saved successfully!')
        return redirect('product_list')
    return redirect('cart_view')
