"""meteorological URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from app import views
from meteorological import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('star_ajax/', views.star_ajax, name='star_ajax'),
    path('my_shoucang/', views.my_shoucang, name='my_shoucang'),
    path('type2sql/', views.type2sql, name='type2sql'), # 入库
    path('detail/', views.detail, name='detail'),
    path('test/', views.test, name='test'),
    path('search/', views.search, name='search'),
    path('plot/', views.plot, name='plot'),



    path('scrawlNew/', views.scrawlNew, name='scrawlNew'),# shou手动爬取数据
    path('scrawl_ajax/', views.scrawl_ajax, name='scrawl_ajax'), # 爬取数据
    path('tuijian/', views.tuijian, name='tuijian'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
