from django.shortcuts import render
from order.models import Order


def view_stocks(request):
    product_and_stocks = Order.objects.all()
    return render(request, template_name='index.html', context={
        'orders': product_and_stocks,
    })
