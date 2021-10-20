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
from .views import *

app_name = 'sales'
urlpatterns = [
    path('customer/new/', CustomerCreateView.as_view(), name="customer-create"),
    path('customer/list/', CustomerListView.as_view(), name="customer-list"),
    path('customer/update/<int:pk>/', CustomerUpdateView.as_view(), name="customer-update"),
    path('customer/detail/<int:pk>/', CustomerDetailView.as_view(), name="customer-detail"),
    path('customer/delete/<int:pk>/', CustomerDeleteView.as_view(), name="customer-delete"),

    path('plan-type/new/', PlanTypeCreateView.as_view(), name="plan-type-create"),
    path('plan-type/list/', PlanTypeListView.as_view(), name="plan-type-list"),
    path('plan-type/update/<int:pk>/', PlanTypeUpdateView.as_view(), name="plan-type-update"),
    path('plan-type/detail/<int:pk>/', PlanTypeDetailView.as_view(), name="plan-type-detail"),
    path('plan-type/delete/<int:pk>/', PlanTypeDeleteView.as_view(), name="plan-type-delete"),

    path('plan/new/', create_sales_plan, name='create-sales-plan-header'),
    path('plan/list/', ListSalesPlanHeader.as_view(), name='list-sales-plan-headers'),
    path('plan/details/<int:pk>/', SalesPlanDetailView.as_view(), name='details-sales-plan'),
    path('plan/delete/<int:pk>/', SalesPlanDeleteView.as_view(), name="delete-sales-plan"),
    path('plan/edit/<int:pk>/', UpdateSalesPlanHeader.as_view(), name='edit-sales-plan-header'),
    path('plan/edit/<int:pk>/items/', sales_plan_items, name='sales-plan-items'),
    path('plan/edit/<int:pk>/items/update/', update_plan_items, name='sales-plan-items-update'),
    path('plan/list/items/', ListPlanItems.as_view(), name='list-sales-plan-items'),
    path('records/<int:pk>/', sales_records_lookup, name='sales-records-lookup'),
    path('plan/lookup/<int:pk>/', sales_plans_lookup, name='sales-plan-lookup'),

    path('upload-data/', upload_data_view, name='upload-data'),

]
