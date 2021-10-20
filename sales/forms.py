from django import forms
from django import forms
from django.db.models import fields
from django.forms import widgets
from django.forms.formsets import formset_factory
from .models import *


class UploadDataForm(forms.ModelForm):
    class Meta:
        model = UploadData
        fields = ('file_name',)

class PlanItemForm(forms.ModelForm):
    previous_qty = forms.CharField(widget = forms.TextInput(attrs={'readonly':'readonly'}))
    
    
    class Meta:
        model = PlanItem
        fields = '__all__'
        widgets = {
            'sales_plan': forms.HiddenInput(),
            
        }


PlanItemFormSet = formset_factory(PlanItemForm, extra=0)



class PlanItemFormDefault(forms.ModelForm):
   
    class Meta:
        model = PlanItem
        fields = '__all__'
        widgets = {
            'sales_plan': forms.HiddenInput(),
            
        }


class SalesPlanForm(forms.ModelForm):
    class Meta:
        model = SalesPlan
        fields = '__all__'


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            
        }

class PlanTypeForm(forms.ModelForm):
    class Meta:
        model = PlanType
        fields = '__all__'
        widgets = {
            
        }