from django.conf.urls import url

from .views import (
    ProductListView,
    product_detail_view,
    ProductDetailSlugView,
    )

urlpatterns = [
    # views from product app
    url(r'^$', ProductListView.as_view(),name='list'),
    url(r'^(?P<pk>\d+)/$', product_detail_view, name='detail'),    
     
]
