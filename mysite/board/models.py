
from django.db import models
from django.utils import timezone
import datetime
from bokeh.themes import default

class Stocklist(models.Model):
    stock_id = models.CharField(max_length=6, primary_key=True)
    stock_name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.stock_name

class Stock(models.Model):
    stock = models.ForeignKey(Stocklist, default=None, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    price = models.IntegerField(default=0)   
    max_price = models.IntegerField(default=0)
    min_price = models.IntegerField(default=0)
    sales_amount = models.IntegerField(default=0)
    updown = models.IntegerField(default=None)
    updown_percentage = models.FloatField(default=None)
    
    class Meta:
        ordering = ['stock','-date','-updown_percentage']
        unique_together = ['stock', 'date']

    
    def __str__(self):
        return self.stock.stock_id
    
class Article(models.Model):
    stock = models.ForeignKey(Stocklist, default=None, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    date = models.DateField(null=True,blank=True, default=None)#주석은 첫번째 인수
    keyword = models.TextField(null=True)
    
    class Meta:
        ordering = ['-date', 'stock']
        unique_together = ['stock','title','date']
    
    def __str__(self):
        return self.title
    
    def was_written_recently(self):
        return self.date1 >= timezone.now() - datetime.timedelta(days=1)
    
