from django.contrib import admin
from django.urls import path

from . import views

app_name = 'myapp'

urlpatterns = [
    path('', admin.site.urls),
    # path('myapp/CreatorInfo',back_to_list),
]
