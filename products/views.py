from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product
from django.utils import timezone


def home(request):
    products = Product.objects.order_by('-votes_total')
    return render(request, 'products/home.html', {'products': products})


@login_required
def create(request):
    if request.method == "POST":
        if request.POST['title'] and request.POST['body'] and request.POST['url']:
            product = Product()
            try:
                product.icon = request.FILES['icon']
                product.image = request.FILES['image']
            except Exception as error:
                return render(request, 'products/create.html', {'error': 'An attachment is missing:', 'actual_error': error})
            product.title = request.POST['title']
            product.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = 'http://' + request.POST['url']
            product.pub_date = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error': 'All fields are required'})
    else:
        return render(request, 'products/create.html')


def details(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/details.html', {'product': product})


@login_required(login_url="/accounts/signup")
def upvote(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        product.votes_total += 1
        product.save()
        return redirect('/products/' + str(product.id))
