import random
import string
import stripe
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product,Available,Order
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings
from django.utils.decorators import method_decorator
from .decorators import admin_required,customer_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone



# mail functionality can also be generated in future,simply by using django's send_mail.

@method_decorator([login_required, admin_required], name='dispatch')
class AvailableCreateView(CreateView):
    model=Available
    template_name='products/available.html'
    fields=['rooms_available','product']
    def form_valid(self,form):
        instance=form.save(commit=False)
        instance.save()
        return redirect('home')

class HomePageView(LoginRequiredMixin,ListView):
    template_name='products/home.html'
    model = Product
    context_object_name='products'

    def get_queryset(self):
        products = super().get_queryset()
        return products

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['availables'] = Available.objects.all()
        return context




@method_decorator([login_required, admin_required], name='dispatch')
class ProductCreateView(CreateView):
    model=Product
    template_name='products/create.html'
    fields=['roomtype','description','image','price']
    def form_valid(self,form):
        instance=form.save(commit=False)
        instance.save()
        return redirect('home')

@method_decorator([login_required, admin_required], name='dispatch')
class ProductUpdateView(UpdateView):
    model=Product
    template_name='products/update.html'
    fields=['roomtype','description','image','price']
    def form_valid(self,form):
        instance=form.save()
        return redirect('/',instance.pk)


@method_decorator([login_required, admin_required], name='dispatch')
class ProductDeleteView(DeleteView):
    model=Product
    template_name='products/delete.html'
    fields=['roomtype','description','image','price']
    success_url='/'




@login_required(login_url="/accounts/signup")
def detail(request,product_id):
    product=get_object_or_404(Product, pk=product_id)
    return render(request,'products/detail.html',{'product':product})


@login_required(login_url="/accounts/signup")
def upvote(request,product_id):
    if request.method=="POST":
        product=get_object_or_404(Product , pk=product_id)
        product.votes_total +=1
        product.save()
        return redirect('/products/' + str(product.id))

def search(request):
    if request.GET:
        search_term= request.GET['search_term']
        search_results= Product.objects.filter(roomtype__icontains=search_term) | Product.objects.filter(price__icontains=search_term)
        availables=Available.objects.all()

        context={
        'search_term': search_term,
        'products': search_results,
        'availables':availables
        }
        return render(request,'products/search.html',context)
    else:
        return redirect('/')



class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.filter(user=self.request.user, ordered=True)
            context = {
                'object': order
            }
            return render(self.request, 'products/order_summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("/")



@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order,created =  Order.objects.get_or_create(
             product=product,
             user=request.user,
             ordered=True
        )

    if order:
        order.quantity += 1
        order.save()
        messages.info(request, "This item quantity was updated.")
        return redirect("order-summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.save()
        messages.info(request, "This item was added to your cart.")
        return redirect("order-summary")



@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order_qs = Order.objects.filter(
        product=product,
        user=request.user,
        ordered=True
    )
    if order_qs.exists():
        order = order_qs[0]
        order.delete()
        messages.info(request, "This item was removed from your cart.")
        return redirect("order-summary")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product", str(product.id))


@login_required
def remove_single_item_from_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=True
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.quantity > 1:
            order.quantity -= 1
            order.save()
        else:
            order.delete()
        messages.info(request, "This item quantity was updated.")
        return redirect("order-summary")
    else:
        messages.info(request, "You do not have an active order")
        return redirect("product", str(product.id))
