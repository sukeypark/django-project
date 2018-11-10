# -*- coding:utf-8 -*-
from django.contrib import admin
from .models import Article
from .models import Stock
from .crawler import crawl_stock, csv_article, crawl_article_url, crawl_article, csv_stock
from django.conf.urls import url
from django.template.response import TemplateResponse
from django.http import HttpResponse
from templates.commons.admin import admin_site
from django.shortcuts import redirect

class AdminStock(admin.ModelAdmin):
    change_list_template = 'admin/board/stock/change_list.html'
    list_display = ('stock','date','price')
    ordering = ('stock','-date')
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url('^update_stock/$', self.admin_site.admin_view(self.update_stock)),
        ]
        return my_urls + urls

    def update_stock(self, request):
        crawl_stock()
        #csv_stock()
        return redirect('/admin/board/stock/')

    
class AdminArticle(admin.ModelAdmin):
    list_display = ('stock','date', 'url', 'title', 'keyword')
    ordering = ('-date','stock')
    change_list_template = 'admin/board/article/change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url('^update_article/$', self.admin_site.admin_view(self.update_article)),
        ]
        return my_urls + urls

    def update_article(self, request):
        crawl_article_url()
        crawl_article()
        #csv_article()
        return redirect('/admin/board/article/')
    
admin_site.register(Article, AdminArticle)
admin_site.register(Stock, AdminStock)