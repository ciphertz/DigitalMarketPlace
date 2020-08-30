import os
from mimetypes import guess_type
from django.conf import settings
from wsgiref.util import FileWrapper
from django.http import Http404,HttpResponse
from django.views.generic import View
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from cart.mixins import MultiSlugMixin
from products.models import Product
from shopping_cart.models import Order
from .models import Profile

@login_required()
def my_profile(request):
	my_user_profile = Profile.objects.filter(user=request.user).first()
	my_orders = Order.objects.filter(is_ordered=True, owner=my_user_profile)
	context = {
		'my_orders': my_orders
	}

	return render(request, "profile.html", context)




class ProductDownloadView(MultiSlugMixin,View):
	model = Product
	template_name = "profile.html"

	def get(self, request, *args, **kwargs):
		obj = self.get_object()
		if obj in request.user.profile.ebooks.all():
			filepath = os.path.join(settings.MEDIA_ROOT, obj.download.path)
			guessed_type = guess_type(filepath)[0]
			wrapper = FileWrapper(open(filepath,'rb'))
			mimetype = 'application/force-download'
			if guessed_type:
				mimetype = guessed_type
			response = HttpResponse(wrapper, content_type=mimetype)
			#if not request.GET.get("preview"):
			response["Content-Disposition"] = "attachment; filename=%s" %(obj.download.name)

			response["X-SendFile"] = str(obj.download.name)
			return response
		else:
			raise Http404
