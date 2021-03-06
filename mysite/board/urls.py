from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from . import views, admin
from django.contrib.auth import views as auth_views


app_name = 'board'
urlpatterns = [
    url('^$', views.index, name='index'),
    url('^chart/$', views.chart, name='chart'),
    url('^chart/(?P<stock_id>\w{6})/$', views.chart, name='chart_selected'),
    url('^chart/(?P<stock_id>\w{6})/(?P<date1>\d{4}\-\d{2}\-\d{2})/(?P<date2>\d{4}\-\d{2}\-\d{2})/$', views.chart, name='chart_search'),
    url('^chart/my_stock/$', views.my_stock, name='my_stock'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)