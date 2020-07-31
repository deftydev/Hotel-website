from django.urls import path, include
from . import views

urlpatterns = [
      path('create/', views.ProductCreateView.as_view() ,name='create'),
      path('available/', views.AvailableCreateView.as_view() ,name='available'),
      path('update/<int:pk>', views.ProductUpdateView.as_view() ,name='update'),
      path('delete/<int:pk>', views.ProductDeleteView.as_view() ,name='delete'),
      path('<int:product_id>', views.detail ,name='detail'),
      path('<int:product_id>/upvote', views.upvote ,name='upvote'),
      path('search/', views.search ,name='search'),
      path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add-to-cart'),
      path('order-summary/', views.OrderSummaryView.as_view(), name='order-summary'),
      path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove-from-cart'),
      path('remove-item-from-cart/<int:product_id>/', views.remove_single_item_from_cart,
         name='remove-single-item-from-cart'),


]
