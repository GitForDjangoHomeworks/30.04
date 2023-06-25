from django.urls import path
from .views import AllProductsView, BbCodeCreateView
app_name = 'pages'

urlpatterns = [
    path('all_products', AllProductsView.as_view(), name='all_products'),
    path('bbcode_create', BbCodeCreateView.as_view(), name='bbcode_create')
 ]