from django.contrib import admin
from django.urls import path

from . import views

app_name = 'myapp'

urlpatterns = [
    path('', admin.site.urls),
    path('blogs/',views.bloglist,name='blogs'),
    path('creatorinfo/',views.fanlist,name='creatorinfo'),
    path('creatorinfo/<int:id>/change/', views.detail, name='creator_profile'),
    path('bloginfo/<int:id>/change/', views.blogDetail, name='blogDetail'),

    # path('myapp/CreatorInfo',back_to_list),
]
