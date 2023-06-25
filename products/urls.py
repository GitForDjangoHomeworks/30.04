from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    SingleProductPageDetailView,
    CategoryDetailView,
    products_bulk_edit,
    ProductImageBulkEditListView,
    ProductNameAmmountPriceAPIView,
    CategoryAPIView
)
router = DefaultRouter()
router.register('edit_category', CategoryAPIView, basename='edit_category')


app_name = 'products'

urlpatterns = [
    path('single_product/<int:pk>', SingleProductPageDetailView.as_view(), name='show_single_product_page'),
    path('products_bulk_edit/', products_bulk_edit, name='products_bulk_edit'),
    path('category/<int:pk>', CategoryDetailView.as_view(), name='category_view'),
    path('product_images_bulk_edit/', ProductImageBulkEditListView.as_view(), 
                                    name = 'product_image_bulk_edit'),
    path('<int:pk>/product_name_price_ammount/',ProductNameAmmountPriceAPIView.as_view(), 
                                                name='product_name_price_ammount_api' ),
    
]
urlpatterns += router.urls