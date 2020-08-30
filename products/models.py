# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.db import models
from sellers.models import SellerAccount

protected_loc = settings.MEDIA_ROOT

def download_loc(instance,filename):
    return "%s/%s" %(instance.slug, filename)
    # if instance.user.username:
    #     return "%s/download/%s" %(instance.user.username,filename)
    # else:
    #     return "%s/download/%s" %("default",filename)

class Product(models.Model):
    seller = models.ForeignKey(SellerAccount,on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=500,null=True,blank=True)
    download = models.FileField(upload_to=download_loc,storage=FileSystemStorage(location=protected_loc),null=True,blank=True)
    price = models.DecimalField(max_digits=60,decimal_places=2)
    sale_price = models.DecimalField(max_digits=60,decimal_places=2,null=True,blank=True)
    slug= models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def get_price(self):
        if self.sale_price:
            return (self.sale_price)
        else:
            return (self.price)

    def get_featured_image(self):
        try:
            images = self.productimage_set.all()
        except:
            return None
        for i in images:
            if i.featured_image:
                return i.image
            else:
                return None

    def is_active(self):
        return self.active

    def get_edit_url(self):
    	view_name = "sellers:product_edit"
    	return reverse(view_name, kwargs={"pk": self.id})


    def get_absolute_url(self,):
        return reverse('products:single_product',args=[self.slug])


    def get_download(self):
        view_name = "accounts:download_slug"
        url = reverse(view_name, kwargs={"slug": self.slug})
        return url

class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/image/")
    title = models.CharField(max_length=120,null=True,blank=True)
    featured_image = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)


    def __str__(self):
        return str(self.title)
#

class Tag(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    tag = models.CharField(max_length=20)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)


    def __str__(self):
        return str(self.tag)
#
#
#
class Category(models.Model):
    product = models.ManyToManyField(Product)
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=500)
    slug = models.SlugField()
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)


    def __str__(self):
        return str(self.title)
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    def get_absolute_url(self):
        return reverse('products:category',args=[self.slug])
#
#
class CategoryImage(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/image/")
    title = models.CharField(max_length=120,null=True,blank=True)
    featured_image = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True,auto_now=False)
    updated = models.DateTimeField(auto_now_add=False,auto_now=True)


    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Category Image"
        verbose_name_plural = "Category Images"
#
class FeaturedManager(models.Manager):
    def get_featured_instance(self):
        items = super(FeaturedManager, self).filter(date_start__lte=datetime.datetime.now()).filter(date_end__gte=datetime.datetime.now())
        print ('items')
        all_items = super(FeaturedManager, self).all()
        if len(items) >= 1:
           return items[0]
        else:
           for i in all_items:
               if i.default:
                   return i
           return all_items[0]
class Featured(models.Model):
    title = models.CharField(max_length=120)
    products = models.ManyToManyField(Product,limit_choices_to={'active':True})
    date_start = models.DateField(auto_now=False,auto_now_add=False)
    date_end = models.DateField(auto_now=False,auto_now_add=False)
    active = models.BooleanField(default=True)
    default = models.BooleanField(default=False)


    def __str__(self):
        return self.title

    def get_featured(self):
        return self.products[:2]

    objects = FeaturedManager()


class ProductRating(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	product = models.ForeignKey(Product,on_delete=models.CASCADE)
	rating = models.IntegerField(null=True, blank=True)
	verified = models.BooleanField(default=False)

	def __str__(self):
		return "%s" %(self.rating)
