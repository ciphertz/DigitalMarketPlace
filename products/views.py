from __future__ import unicode_literals
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Avg,Count
from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse
from shopping_cart.models import Order
from accounts.models import Profile

from .models import Product,Category,ProductImage,ProductRating
from .mixins import ProductManagerMixin
from cart.mixins import (
			LoginRequiredMixin,
			MultiSlugMixin,
			SubmitBtnMixin,
			AjaxRequiredMixin
			)
from sellers.mixins import SellerAccountMixin
from .forms import ProductAddForm, ProductModelForm
from django.views.generic import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

class ProductRatingAjaxView(AjaxRequiredMixin, View):
	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return JsonResponse({}, status=401)

		user = request.user
		product_id = request.POST.get("product_id")
		rating_value = request.POST.get("rating_value")
		exists = Product.objects.filter(id=product_id).exists()
		if not exists:
			return JsonResponse({}, status=404)

		try:
			product_obj = Product.object.get(id=product_id)
		except:
			product_obj = Product.objects.filter(id=product_id).first()

		rating_obj, rating_obj_created = ProductRating.objects.get_or_create(
				user=user,
				product=product_obj
				)
		try:
			rating_obj = ProductRating.objects.get(user=user, product=product_obj)
		except ProductRating.MultipleObjectsReturned:
			rating_obj = ProductRating.objects.filter(user=user, product=product_obj).first()
		except:
			#rating_obj = ProductRating.objects.create(user=user, product=product_obj)
			rating_obj = ProductRating()
			rating_obj.user = user
			rating_obj.product = product_obj
		rating_obj.rating = int(rating_value)
		myproducts = user.profile.ebooks.all()

		if product_obj in myproducts:
			rating_obj.verified = True
		# verify ownership
		rating_obj.save()

		data = {
			"success": True
		}
		return JsonResponse(data)

class ProductCreateView(SellerAccountMixin, SubmitBtnMixin, CreateView):
	model = Product
	template_name = "form.html"
	form_class = ProductModelForm
	#success_url = "/products/"
	submit_btn = "Add Product"

	def form_valid(self, form):
		seller = self.get_account()
		form.instance.seller = seller
		valid_data = super(ProductCreateView, self).form_valid(form)
		#tags = form.cleaned_data.get("tags")
		# if tags:
		# 	tags_list = tags.split(",")
		# 	for tag in tags_list:
		# 		if not tag == " ":
		# 			new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
		# 			new_tag.products.add(form.instance)
		return valid_data

class ProductUpdateView(ProductManagerMixin,SubmitBtnMixin, MultiSlugMixin, UpdateView):
	model = Product
	template_name = "form.html"
	form_class = ProductModelForm
	#success_url = "/products/"
	submit_btn = "Update Product"
	def get_initial(self):
		initial = super(ProductUpdateView,self).get_initial()
		print (initial)
		# tags = self.get_object().tag_set.all()
		# initial["tags"] = ", ".join([x.title for x in tags])
		"""
		tag_list = []
		for x in tags:
			tag_list.append(x.title)
		"""
		return initial
	def form_valid(self, form):
		valid_data = super(ProductUpdateView, self).form_valid(form)
		# tags = form.cleaned_data.get("tags")
		# obj = self.get_object()
		# obj.tag_set.clear()
		# if tags:
		# 	tags_list = tags.split(",")
        #
		# 	for tag in tags_list:
		# 		if not tag == " ":
		# 			new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
		# 			new_tag.products.add(self.get_object())
		return valid_data

class SellerProductListView(SellerAccountMixin, ListView):
	model = Product
	template_name = "sellers/product_list_view.html"

	def get_queryset(self, *args, **kwargs):
		qs = super(SellerProductListView, self).get_queryset(**kwargs)
		qs = qs.filter(seller=self.get_account())
		query = self.request.GET.get("q")
		if query:
			qs = qs.filter(
					Q(name__icontains=query)|
					Q(description__icontains=query)
				).order_by("name")
		return qs

@login_required
def product_list(request):
    object_list = Product.objects.all()
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
    	user_order = filtered_orders[0]
    	user_order_items = user_order.items.all()
    	current_order_products = [product.product for product in user_order_items]

    context = {
        'object_list': object_list,
        'current_order_products': current_order_products
    }

    return render(request, "products/product.html", context)


@login_required()
def single(request,slug):
    product = Product.objects.get(slug=slug)
    object_list = Product.objects.all()
    my_rating = []
    images = product.productimage_set.all()
    categories = product.category_set.all()
    rating_avg = product.productrating_set.aggregate(Avg("rating"), Count("rating"))
    if request.user.is_authenticated:
	    rating_obj = ProductRating.objects.filter(user=request.user, product=product)
	    if rating_obj.exists():
		    my_rating =  rating_obj.first().rating

    related = []
    if len(categories) >=1:
        for category in categories:
            products_category = category.product.all()
            for item in products_category:
                if not item == product:
                    related.append(item)
    filtered_orders = Order.objects.filter(owner=request.user.profile, is_ordered=False)
    current_order_products = []
    if filtered_orders.exists():
	    user_order = filtered_orders[0]
	    user_order_items = user_order.items.all()
	    current_order_products = [product.product for product in user_order_items]

    context = {
        "product":product,
        "categories":categories,
        "edit":True,
        "images":images,
        "related":related,
		"rating_avg":rating_avg,
		"my_rating":my_rating,
		"object_list":object_list,
		"current_order_products":current_order_products
    }
    return render(request,"products/product-detail.html",context)
#
# def search(request):
#     q = request.GET.get('q', '')
#
#     product_queryset = Product.objects.filter(
#         Q(name__icontains=q)|
#         Q(description__icontains=q)
#     )
#     category_queryset = Category.objects.filter(
#         Q(title__icontains=q)|
#         Q(description__icontains=q)
#     )
#     results = list(chain(product_queryset,category_queryset))
#     context = {
#         'query': q,
#         'product_queryset':product_queryset,
#         'category_queryset':category_queryset,
#         'results':results,
#     }
#
#     return render(request,"products/search.html", context)
def search(request):
    try:
        q = request.GET.get('q', '')
    except:
        q = False
    if q:
        query = q
    else :
        query = None


    product_queryset = Product.objects.filter(
        Q(name__icontains=q)|
        Q(description__icontains=q)
    )
    category_queryset = Category.objects.filter(
        Q(title__icontains=q)|
        Q(description__icontains=q)
    )
    results = list(chain(product_queryset,category_queryset))
    context = {
        'query':query,
        'product_queryset':product_queryset,
        'category_queryset':category_queryset,
        'results':results,
    }

    return render(request,"products/search.html", context)

def category_single(request,slug):
    try:
        category = Category.objects.get(slug=slug)
    except:
        raise Http404
    products = category.product.all()
    related = []
    for item in products:
        product_categories = item.category_set.all()
        for single_category in product_categories:
            if not single_category == category:
                related.append(single_category)
    context = {
        'category':category,
        'products':products,
        'related':related,
    }
    return render(request,"products/category.html",context)
