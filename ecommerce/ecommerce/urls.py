"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView

from accounts.views import LoginView, RegisterView, guest_register_view
from addresses.views import (checkout_address_create_view,
                             checkout_address_reuse_view)
from billing.views import payment_method_createview, payment_method_view
from carts.views import cart_detail_api_view
from marketing.views import MailchimpWebhookView, MarketingPreferenceUpdateView

from .views import contact_page, home_page

urlpatterns = [
    url(r'^$', home_page, name='home'),
    url(r'^register/guest/$', guest_register_view, name='guest_register'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^contact/$', contact_page, name='contact'),    
    url(r'^admin/', admin.site.urls),


    # views from accounts app
    url(r'^account/', include("accounts.urls", namespace='account')),
    url(r'^accounts/$', RedirectView.as_view(url='/account')),
    url(r'^settings/$', RedirectView.as_view(url='/account')),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^login/$', LoginView.as_view(), name='login'),
        # accounts passwords
    url(r'^accounts/', include("accounts.passwords.urls")),
    # views from product app
    url(r'^products/', include("products.urls", namespace='products')),
    # views from search app
    url(r'^search/', include("search.urls", namespace='search')),
    # views from carts app
    url(r'^cart/', include("carts.urls", namespace='cart')),
    url(r'^api/cart/', cart_detail_api_view, name='api-cart'),
    # view from address app
    url(r'^checkout/address/create/$',checkout_address_create_view,name='checkout_address_create'),
    url(r'^checkout/address/reuse/$',checkout_address_reuse_view,name='checkout_address_reuse'),
    # views from billing app
    url(r'^billing/payment-method/$', payment_method_view, name='billing-payment-method'),
    url(r'^billing/payment-method/create/$', payment_method_createview, name='billing-payment-method-endpoint'),
    # views from Marketing app
    url(r'^settings/email/', MarketingPreferenceUpdateView.as_view(), name='marketing-pref'),
    url(r'^webhooks/mailchimp/', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),



]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
