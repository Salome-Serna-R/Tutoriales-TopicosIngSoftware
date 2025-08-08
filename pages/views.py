from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView, ListView, View
from django.views.generic.edit import CreateView
from django import forms
from django.urls import reverse, reverse_lazy
from django.core.validators import MinValueValidator
from .models import Product


# Creación de constantes para no repetir strings
TITLE_PRODUCTS = "Products - Online Store"
SUBTITLE_PRODUCTS = "List of products"



class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class AboutPageView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "About us - Online Store",
            "subtitle": "About us",
            "description": "This is an about page ...",
            "author": "Developed by: Your Name",
        })
        return context


class ContactPageView(TemplateView):
    template_name = 'pages/contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "title": "Contact us - Online Store",
            "subtitle": "Contact us",
            "email": "eafit@example.edu.co",
            "address": "Eafit university, Somewhere, World",
            "phone": "+57 (555) 123-4567",
        })
        return context



class ProductIndexView(View):
    template_name = 'products/index.html'

    def get(self, request):
        context = {
            "title": TITLE_PRODUCTS,
            "subtitle": SUBTITLE_PRODUCTS,
            "products": Product.objects.all()
        }
        return render(request, self.template_name, context)


class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product = get_object_or_404(Product, pk=int(id))
        except (ValueError, Product.DoesNotExist):
            return HttpResponseRedirect(reverse('home'))

        context = {
            "title": f"{product.name} - Online Store",
            "subtitle": f"{product.name} - Product information",
            "product": product
        }
        return render(request, self.template_name, context)


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': TITLE_PRODUCTS,
            'subtitle': SUBTITLE_PRODUCTS
        })
        return context


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']
        # Validación directa en el form
        validators = {
            'price': [MinValueValidator(0.01)]
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'products/create.html'
    success_url = reverse_lazy('product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Create product"
        return context
