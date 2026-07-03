from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('rooms/kitchen/', views.kitchen, name='kitchen'),
    path('rooms/bathroom/', views.bathroom, name='bathroom'),
    path('rooms/bedroom/', views.bedroom, name='bedroom'),
    path('rooms/living_room/', views.living_room, name='living_room'),
    path('product/<int:product_id>/',
    views.product_detail, name='product_detail'),
    path('cart/', views.cart, name='cart'),
    path('add-to-cart/<int:product_id>/',
    views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:product_id>/',
    views.remove_from_cart, name='remove_from_cart'),
    path('get-cart-count/', views.get_cart_count, name='get_cart_count'),
    path('update-cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('get-cart-quantity/<int:product_id>/', views.get_cart_quantity, name='get_cart_quantity',),
    path('checkout/', views.checkout, name='checkout'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('smart-planner/', views.smart_planner, name='smart_planner'),
    path('order-success/', views.order_success, name='order_success'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('order/<int:order_id>/', views.order_details, name='order_details',),
   
]

  