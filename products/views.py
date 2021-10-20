from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from products.models import *
from django.urls import reverse_lazy

# Create your views here.


class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('products:list-product')


class ProductListView(ListView):
    model = Product
    ordering = ['product_subgroup', 'code', 'weight']


class ProductUpdateView(UpdateView):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('products:list-product')


class ProductDetailView(DetailView):
    model = Product


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('products:list-product')