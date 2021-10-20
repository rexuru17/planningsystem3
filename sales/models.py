from django.db import models
from products.models import *
from django.db.models import Sum, Avg, Max, Min, constraints
from django.urls import reverse
import calendar
import datetime



# Create your models here.
class SalesChannel(models.Model):
    code = models.CharField(max_length=5, primary_key=True, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code', 'name'], name='%(app_label)s_%(class)s_is_unique'),

        ]


class Customer(models.Model):
    code = models.CharField(max_length=6, primary_key=True, unique=True)
    name = models.CharField(max_length=100)
    sales_channel = models.ForeignKey(SalesChannel, on_delete=models.RESTRICT)
    portfolio = models.ManyToManyField(Product, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    include_in_channel_planning = models.BooleanField(default=False)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['code', 'name'], name='%(app_label)s_%(class)s_is_unique'),

        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('sales:customer-detail', kwargs={'pk': self.pk})


class PlanType(models.Model):
    
    def year_choices():
        return [(r,r) for r in range(datetime.date.today().year, datetime.date.today().year+10)]

    def current_year():
        return datetime.date.today().year

    PLAN_CHOICES = (("FORECAST", "Forecast"), ("BUDGET", "Budget"))
    name = models.CharField(max_length=50, unique=True, choices=PLAN_CHOICES)
    year = models.IntegerField(choices=year_choices(), default=current_year)

    def __str__(self):
        info = str(self.name) + ' - ' + str(self.year)
        return str(info)


class SalesPlan(models.Model):
    MONTH_CHOICES = [(str(i), calendar.month_name[i]) for i in range(1,13)]
    period = models.CharField(max_length=20, choices=MONTH_CHOICES, default='1')
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT)
    plan_type = models.ForeignKey(PlanType, on_delete=models.RESTRICT)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['period', 'customer', 'plan_type'], name='%(app_label)s_%(class)s_is_unique'),
        ]
           

    def __str__(self):
        info = str(self.plan_type) + ' - ' + str(self.customer) + ' - ' + str(self.period)
        return str(info)

    @property
    def month(self):
        for choice in self.MONTH_CHOICES:
            if self.period == choice[0]:
                return choice[1]


class PlanItem(models.Model):
    sales_plan = models.ForeignKey(SalesPlan, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sales_plan', 'product'], name='%(app_label)s_%(class)s_is_unique'),

        ]

    @property
    def previous_qty(self):
        period = self.sales_plan.period
        year = datetime.date.today().year
        records = SalesRecords.objects.filter(product=self.product, date__month=period, date__year__range=((year-3), (year-1))).aggregate(Sum('quantity'))
        if records['quantity__sum']:
            return('{:.2f}'.format(float(records['quantity__sum']/3)))
        else:
            return 0

    def __str__(self):
        info = str(self.sales_plan) + ' - ' + str(self.product)
        return str(info)

    def get_creation_url(self):
        kwargs={
            'pk': str(self.sales_plan.pk),            
        }
        return reverse('sales:sales-plan-items', kwargs=kwargs)


class SalesRecords(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField()
    quantity = models.FloatField()


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['customer', 'product', 'date', 'quantity'], name='%(app_label)s_%(class)s_is_unique'),

        ]

    class Meta:
        verbose_name_plural = "Sales Records"

    def __str__(self):
        sales_records_info = str(self.customer) + ' - ' + str(self.date) + ' - ' + str(self.product)
        return str(sales_records_info)

class UploadData(models.Model):
    file_name = models.FileField(upload_to='tmp_data')
    uploaded = models.DateTimeField(auto_now=True)
    activated = models.BooleanField(default=False)

    def __str__(self):
        return f"File id: {self.id}"
