from django.forms.models import modelformset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from products.models import *
from sales.models import *
from sales.forms import *
from django.urls import reverse_lazy
from django.forms import formset_factory
from sales.filters import *
from sales.utils import upload_records
import pandas as pd
# Create your views here.


########### Upload Data Views ######################
def upload_data_view(request):
    form = UploadDataForm(request.POST or None, request.FILES or None)
    
    if form.is_valid():
        form.save()
        form = UploadDataForm()
        obj = UploadData.objects.get(activated=False)
        file_path = obj.file_name.path
        upload_records(file_path=file_path)
        obj.activated = True
        obj.save()
    context = {
        'form': form,
    }
    return render(request, 'sales/upload.html', context)



########### Customer Views ######################


class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
  
  


class CustomerDetailView(DetailView):
    model = Customer
    

class CustomerListView(ListView):
    model = Customer
    ordering = ['sales_channel', 'code',]


class CustomerUpdateView(UpdateView):
    model = Customer
    fields = '__all__'
    success_url = reverse_lazy('sales:customer-list')
    
    
class CustomerDeleteView(DeleteView):
    model = Customer
    success_url = reverse_lazy('sales:customer-list')
########### Sales Plan Type Views ######################


class PlanTypeCreateView(CreateView):
    model = PlanType
    form_class = PlanTypeForm
  
  
class PlanTypeDetailView(DetailView):
    model = PlanType
    

class PlanTypeListView(ListView):
    model = PlanType


class PlanTypeUpdateView(UpdateView):
    model = PlanType
    fields = '__all__'
    success_url = reverse_lazy('sales:plan-type-list')
    
    
class PlanTypeDeleteView(DeleteView):
    model = PlanType
    success_url = reverse_lazy('sales::plan-type-list')


########### Sales Plan Views ######################
def create_sales_plan(request):
    form = SalesPlanForm(request.POST or None)
    if form.is_valid():
        obj = form.save()
        plan_item = PlanItem(sales_plan=obj)
        return redirect(plan_item.get_creation_url())
    context = {
        'form': form
    }
    return render(request, 'sales/salesplan_form.html', context)



class ListSalesPlanHeader(ListView):
    model = SalesPlan
    

class UpdateSalesPlanHeader(UpdateView):
    model = SalesPlan
    fields = '__all__'
    success_url = reverse_lazy('sales:list-sales-plan-headers')


def sales_plan_items(request, pk):
    plan_header = get_object_or_404(SalesPlan, id=pk)
    customer = plan_header.customer
    portfolio = customer.portfolio.all()
    initial = []
    for item in portfolio:
        initial.append({'sales_plan':plan_header, 'product':item, 'quantity':0, 'previous_qty': PlanItem(sales_plan=plan_header, product=item).previous_qty})
    PlanItemFormset = formset_factory(PlanItemForm, extra=0)
    formset = PlanItemFormset(initial=initial)
    if request.method == "POST":
        formset = PlanItemFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                quantity = form.cleaned_data['quantity']
                form.save()
                # if quantity > 0 :
                #     form.save()                   
            return redirect('sales:list-sales-plan-items')
    context = {
        'formset':formset,
        'customer': customer,
        'plan': plan_header,

    }
    return render(request, 'sales/plan-create.html', context)


class ListPlanItems(ListView):
    model = PlanItem

class PlanItemUpdateView(UpdateView):
    model = PlanItem
    form_class = PlanItemForm
    formset_class = PlanItemFormSet


def update_plan_items(request, pk):
    plan_header = get_object_or_404(SalesPlan, id=pk)
    queryset = PlanItem.objects.filter(sales_plan=plan_header)
    PlanItemFormset = modelformset_factory(PlanItem, form=PlanItemFormDefault, extra=0)
    formset = PlanItemFormset(request.POST or None, queryset=queryset)
    if formset.is_valid():
        instances = formset.save()        
        return redirect('sales:list-sales-plan-items')
    context = {
        'formset': formset,
        'plan': plan_header,
    }
    return render(request, 'sales/plan-edit.html', context)


class SalesPlanDetailView(DetailView):
    model = SalesPlan


   
class SalesPlanDeleteView(DeleteView):
    model = SalesPlan
    success_url = reverse_lazy('sales:list-sales-plan-headers')

########### Sales Records Views ######################

"""
Work on filtering data correctly for customers
"""
def sales_records_lookup(request, pk):
    customer = Customer.objects.get(code=pk)
    sales_records = customer.salesrecords_set.all()
    myFilter = SalesRecordsFilter(request.GET, queryset=sales_records)
    sales_records = myFilter.qs

    context = {
        'customer': customer,
        'sales_records': sales_records,
        'myFilter': myFilter,
    }
    return render(request, 'sales/salesrecords_lookup.html', context)

def sales_plans_lookup(request, pk):
    customer = Customer.objects.get(code=pk)
    plans = customer.salesplan_set.all()
    myFilter = SalesPlanFilter(request.GET, queryset=plans)
    plans = myFilter.qs
    x = plans.values('planitem__product__code', 'planitem__product__name', 'planitem__quantity', 'customer__name', 'plan_type__name', 'period')
    df = pd.DataFrame(x)
    pivot = df.pivot_table(index=['planitem__product__code', 'planitem__product__name'], columns=['period'], values='planitem__quantity', aggfunc=sum)
    context = {
        'customer': customer,
        'plans': plans,
        'myFilter': myFilter,
        'data': pivot.to_html()
    }
    return render(request, 'sales/salesplan_lookup.html', context)
