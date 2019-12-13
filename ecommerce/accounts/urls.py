from django.conf.urls import url

from .views import (
    AccountHomeView,
    )

urlpatterns = [
    # views from account app
    url(r'^$', AccountHomeView.as_view(),name='home'),  
     
]
