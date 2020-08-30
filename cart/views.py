import os
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from shopping_cart.models import Order
from products.models import Featured

def about(request):
    return render(request,"about.html",{})

def contact(request):
    return render(request,"contact.html",{})

#@login_required()
def home(request):
    featured_products = []
    featured = Featured.objects.get_featured_instance()
    for i in featured.products.all():
        featured_products.append(i)
    # filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    # current_order_products = []
    # if filtered_orders.exists():
    # 	user_order = filtered_orders[0]
    # 	user_order_items = user_order.items.all()
    # 	current_order_products = [product.product for product in user_order_items]
    # if cart:
    #     cartitems = []
    #     for item in cart.cartitem_set.all():
    #         cartitems.append(item.product)
    template= "index.html"
    context={
        'featured_products':featured_products,
        'featured':featured,
    }
    return render(request,template,context)
