from django import template
from datetime import datetime
from urllib.parse import urlencode
from django.utils.html import format_html, escape
import math

register = template.Library()

@register.filter
def return_list(x,y):
    return math.ceil(x/y)

@register.filter
def _range(_min, args=None):
    _max, _step = None, None
    if args:
        if not isinstance(args, int):
            _max, _step = map(int, args.split(','))
        else:
            _max = args
    args = filter(None, (_min, _max, _step))
    return range(*args)

@register.filter
def dateFormat(date):
    return date.strtime("%Y.%m.%d %H:%M:%S")
    
@register.filter
def pixelize(x, y):
    return str(x*int(y)) + "px"

@register.filter
def to_int(x):
    return int(x)

@register.filter
def page_move(x,y):
    x = int(x)
    y = int(y)
    if y < 0:
        rtn = ( math.ceil( x / abs(y) ) - 1 ) * 5
        if rtn < 1:
           rtn = 1
        return rtn
    else:
       return math.ceil( x / y ) * 5 + 1
@register.filter
def title_color(x,y):
    html_y = format_html('<font class="w3-orange">{}</font>', escape(y))
    return escape(x).replace(y, html_y)

@register.filter
def content_color(x,y):
    idx = x.find(y)
    first_idx = idx - 25
    pretext = ''

    if first_idx < 0:
        first_idx = 0
    else:
        pretext = '...'
        
    x = x[first_idx:]
    html_y = format_html('<font class="w3-orange">{}</font>', escape(y))
    return escape(x).replace(y, html_y)