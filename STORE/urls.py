from django.urls import path
from .views import *
from . import views 
app_name="STORE"
# from allauth import urls 

urlpatterns = [
path("",views.home,name="home"),
#main pages
path("products/",views.products,name="products"),
path("category/<str:slug>/",views.category,name="category_filter"),
   
## filter_delete
path("filter/color",views.color_filter_delete,name="color_delete"),
path("filter/price",views.price_filter_delete,name="price_delete"),
path("filter/ship",views.ship_filter_delete,name="ship_delete"),
path("filter/size",views.size_filter_delete,name="size_delete"),
path("filter/category",views.category_filter_delete,name="category_delete"),
path("filter/manufacrurer",views.manu_filter_delete,name="manu_delete"),

# Cart
path("add-to-cart/<str:id>/",views.add_to_cart,name="cart_add"),
path("remove-from-cart/<str:id>/",views.remove_from_cart,name="cart_remove"),
path("whislist-add/<str:id>/",views.wishlist_add,name="wishlist_add"),
path("whislist-remove/<str:id>/",views.wishlist_remove,name="wishlist_remove"),


#       Dashboard     
path("dashboard/",views.dashboard,name="dashboard"),
path("products/add",views.add_products,name="products_add"),

]   
          
          

 
 