from django import template
import math
from datetime import datetime, timedelta

register = template.Library()

@register.filter
def colorChange(x):
    if x == 1:
        color = 'w3-red'
    elif x == 2:
        color = 'w3-orange'
    elif x == 3:
        color = 'w3-teal'
    else:
        color = 'w3-blue'
    return color

@register.filter
def updownChange(x):
    if x % 2 != 0:
        updown = 'asc'
    else:
        updown = 'desc'
    return updown

@register.filter
def vote_percentage(value, choice_set):
    sum=0
    for choice in choice_set:
        sum += choice.votes
    if sum == 0:
        return 0
    else:
        return_value = value/sum
        return '{0:.0%}'.format(return_value)

@register.filter()
def to_int(value):
    return int(value)

@register.filter()
def add(x,y):
    x = int(x)
    y = int(y)
    return x + y

@register.filter()
def date_form(x):
    dt = datetime.strptime(x,"%Y-%m-%d")
    return "{}/{}/{}".format(dt.month,dt.day,dt.year)
    
    