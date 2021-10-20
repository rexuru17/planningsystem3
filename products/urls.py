"""planningsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from . import views as product_views


app_name = 'products'
urlpatterns = [
    path('create/', product_views.ProductCreateView.as_view(), name='create-product'),
    path('list/', product_views.ProductListView.as_view(), name='list-product'),
    path('update/<int:pk>/', product_views.ProductUpdateView.as_view(), name='update-product'),
    path('delete/<int:pk>/', product_views.ProductDeleteView.as_view(), name='delete-product'),
    path('detail/<int:pk>/', product_views.ProductDetailView.as_view(), name='detail-product'),

]
