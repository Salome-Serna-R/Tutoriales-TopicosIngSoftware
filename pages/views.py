from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.views import View
from django import forms
from django.shortcuts import render, redirect
from networkx import reverse
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

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

class Product:
    products = [
        {"id":"1", "name":"TV", "description":"Best TV", "price": 100},
        {"id":"2", "name":"iPhone", "description":"Best iPhone", "price": 120},
        {"id":"3", "name":"Chromecast", "description":"Best Chromecast", "price": 35},
        {"id":"4", "name":"Glasses", "description":"Best Glasses", "price": 80}
    ]

class ProductIndexView(View):
    template_name = 'products/index.html'
    
    def get(self, request):
        viewData = {}
        viewData["title"] = "Products - Online Store"
        viewData["subtitle"] = "List of products"
        viewData["products"] = Product.products
        return render(request, self.template_name, viewData)
    


class ProductShowView(View):
    template_name = 'products/show.html'

    def get(self, request, id):
        try:
            product_id = int(id)
            product = next((p for p in Product.products if int(p["id"]) == product_id), None)
            if not product:
                return HttpResponseRedirect(reverse('home'))
        except (ValueError, TypeError):
            return HttpResponseRedirect(reverse('home'))

        viewData = {}
        viewData["title"] = product["name"] + " - Online Store"
        viewData["subtitle"] = product["name"] + " - Product details"
        viewData["product"] = product

        return render(request, self.template_name, viewData)
    


class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)


class ProductForm(forms.Form):
    name = forms.CharField(required=True)
    price = forms.FloatField(required=True)

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

class ProductCreateView(View):
    template_name = 'products/create.html'
    success_template_name = 'products/success.html'

    def get(self, request):
        form = ProductForm()
        viewData = {}
        viewData["title"] = "Create product"
        viewData["form"] = form
        return render(request, self.template_name, viewData)

    def post(self, request):
        form = ProductForm(request.POST)
        if form.is_valid():
            viewData = {
                "title": "Product created",
                "message": "Product created"
            }
            return render(request, self.success_template_name, viewData)
        else:
            viewData = {}
            viewData["title"] = "Create product"
            viewData["form"] = form
            return render(request, self.template_name, viewData)