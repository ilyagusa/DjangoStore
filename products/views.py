from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from products.models import Product, ProductCategory, Basket
# Create your views here.
PER_PAGE = 3


def index(request):
    context = {
        'title': "Store",
    }
    return render(request, 'products/index.html', context)


def products(request, category_id=None, page_number=1):
    fltr_products = Product.objects.filter(category_id=category_id) if category_id else Product.objects.all()

    paginator = Paginator(fltr_products, PER_PAGE)
    products_paginator = paginator.page(page_number)

    context = {
        'title': "Store - Каталог",
        'categories': ProductCategory.objects.all(),
        'products': products_paginator
    }

    return render(request, 'products/products.html', context)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def basket_remove(request, basket_id):
    Basket.objects.get(id=basket_id).delete()

    return HttpResponseRedirect(request.META["HTTP_REFERER"])