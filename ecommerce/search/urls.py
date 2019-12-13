from django.conf.urls import url

from .views import (
    SearchProductView,
    )

urlpatterns = [
    # views from search app
    url(r'^$', SearchProductView.as_view(),name='query'),       
]
