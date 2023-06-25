from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from django.views.generic import ListView, CreateView
from django.views.generic.base import TemplateView
from .models import BbCodeModel
from .forms import BbCodeForm
from products.models import SingleProduct

from icecream import ic
# Create your views here.

class AllProductsView(TemplateView):
    template_name = 'pages/show_page/all_products.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = SingleProduct.objects.prefetch_related('images')
        return context

class BbCodeCreateView(CreateView):
    model = BbCodeModel
    form_class = BbCodeForm
    template_name = 'pages/bbcode/bbcode_create.html'
    success_url = '/'
    # def get(self, request, *args, **kwargs):
    #     return reverse(request, self.template_name, context={})

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save(commit=True)
            return self.form_valid(form)
        else:
            return self.form_invalid(form)