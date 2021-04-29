from django.contrib import admin
from django.urls import path,include

from . import views

urlpatterns = [
    # 页面配置
    path('', admin.site.urls),
    path('go_tp_wc_html/', views.go_tp_wc_html),
    # 接口配置
    path('tp_wordcloud/', views.tp_wordcloud, name="tp_wc"),  # tp:supertopic

]
