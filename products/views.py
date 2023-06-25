from django.shortcuts import render, redirect, get_object_or_404
from precise_bbcode.bbcode import get_parser

from django.views.generic.base import TemplateView
from django.forms import modelformset_factory, inlineformset_factory
from django.forms.formsets import ORDERING_FIELD_NAME
from django.views.generic import ListView, DetailView

#REST 
from rest_framework import generics, viewsets
from .serializers import ProductNameAmmountPriceSerializer, CategorySerializer

from django.db import transaction

from products.models import SingleProduct, Category, ProductImage
from products.forms import ProductForm, ProductImageForm
from icecream import ic
# Create your views here.

class SingleProductPageDetailView(DetailView):
    template_name = 'products/single_product.html'
    context_object_name = 'product'
    model = SingleProduct   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parser = get_parser()
        context['from_view'] = parser.render('[b]Здравствуйте, люди [u]дорогие![/u][/b]')
        return context


class CategoryDetailView(DetailView):
    template_name = 'products/category_view.html'
    context_object_name = 'category'
    model = Category

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = kwargs['object']
        ic(kwargs)
        parser = get_parser()
        context['from_view'] = parser.render(f'[quote][b]Этот каталог {category.name}  [/b][/quote]')
        return context





def products_bulk_edit(request):
    ProductFormSet = modelformset_factory(
        SingleProduct, form=ProductForm, fields=('name', 'description', 'in_store', 'initial_price'),
         extra=1, can_delete=True, can_order=True
    )
    template_name = 'products/product_bulk_edit.html'
    context = {}

    if request.method == 'POST':
        formset = ProductFormSet(request.POST)

        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    save_point = transaction.savepoint()
                    product = form.save(commit=False)
                    product.order = form.cleaned_data[ORDERING_FIELD_NAME]
                    try:

                        product.save()
                        transaction.savepoint_commit(save_point)
                    except:
                        transaction.rollback()
                    transaction.commit()
            return redirect('products:products_bulk_edit')
    else:
        formset = ProductFormSet(queryset=SingleProduct.objects.prefetch_related('images'))
        '''
            Здесь  я использую prefetch_related  к полю images так как там ManyToMany relationship
            prefetch_related нужен чтобы уменьшить колво запросов в базу данных
            а этот метод помогает сразу брать поле images при первом запросе к продукты
        '''
    context['product_form_set'] = formset
    return render(request, template_name, context)


class ProductImageBulkEditListView(TemplateView):
    template_name = 'products/product_image_bulk_edit.html'
    ProductImgaeFormset = modelformset_factory(ProductImage, form=ProductImageForm, 
                        fields=('description', 'image'), can_delete=True, can_order=True, extra=1)
    
    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     queryset['product_images'] = ProductImage.objects.all()
    #     return queryset
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_image_formset'] = self.ProductImgaeFormset(queryset=ProductImage.objects.all())
        return context
    def post(self, request, *args, **kwargs):
        ic('post')
        formset = self.ProductImgaeFormset(request.POST)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data:
                    product_image = form.save(commit=False)
                    product_image.order = form.cleaned_data[ORDERING_FIELD_NAME]
                    product_image.save()
                return redirect('products:product_image_bulk_edit')
        else:
            self.get_context_data()['product_image_formset'] = formset
            ic(formset.errors)
            return render(request, self.template_name, self.get_context_data())

        
#API
class ProductNameAmmountPriceAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SingleProduct.objects.all()
    serializer_class = ProductNameAmmountPriceSerializer

    def get(self, request, *args, **kwargs):
        product = get_object_or_404(SingleProduct, pk=kwargs['pk'])
        product.save()

    
        return self.retrieve(request, *args, **kwargs)

class CategoryAPIView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    