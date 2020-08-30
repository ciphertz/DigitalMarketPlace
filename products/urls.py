from django.conf.urls import url

from .views import (
    product_list,
    single,
    category_single,
    search,
    ProductRatingAjaxView,
    )

app_name = 'products'

urlpatterns = [
    url(r'^$', product_list, name='product-list'),
    url(r'^ajax/rating/$', ProductRatingAjaxView.as_view(), name='ajax_rating'),
    url(r'^category/(?P<slug>.*)/$',category_single,name="category"),
    url(r'^search/', search, name="search"),
    url(r'^(?P<slug>.*)/$',single, name="single_product"),
]


# urlpatterns = patterns('products.views',
#         url(r'^$','list_all',name="all_products"),
#         url(r'^search/','search',name="search"),
#         url(r'^add/','add_product',name="add_product"), #migth be a problem here loook very
#         url(r'^category/(?P<slug>.*)/$','category_single',name="category"),
#         url(r'^(?P<slug>.*)/images/','manage_product_image',name="manage_product_image"),
#         url(r'^(?P<slug>.*)/edit/','edit_product',name="edit_product"),
#         url(r'^(?P<slug>.*)/download/(?P<filename>.*)$','download_product',name="download_product"),
#         url(r'^(?P<slug>.*)/$','single',name="single_product"),
