from django import template

register = template.Library()


@register.simple_tag
def calculateStockProd(quantity,stock):
    result = 0
    if(quantity>0):
        result = int(stock) - int(quantity)
    return result