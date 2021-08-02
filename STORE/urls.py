from django.urls import path
from .views import *
from . import views 
app_name="STORE"
# from allauth import urls 

urlpatterns = [
path("",views.home,name="home"),
path("test/",views.test,name="test"),
 
#main pages
path("products/",views.products,name="products"),
path("category/<str:slug>/",views.category,name="category_filter"),
path("branch/<str:slug>/",views.branch,name="branch_filter"),

path("wishlist/",views.wishlist,name="wishlist"),

path("product/<str:id>/",views.this_product,name="this_product"),
path("cart/",views.cart,name="cart"),
path("order/<str:id>/",views.order,name="order"),
path("empty/",views.empty,name="empty"),   
path("account/<str:slug>/",views.profile,name="profile"), 
path("profile/<str:slug>/",views.profile_account,name="profile_account"),   
path("profile/<str:slug>/edit",views.profile_edit,name="profile_edit"),   

path("address/<str:slug>/",views.address,name="address"),   
path("address/add/<str:slug>/",views.address_add,name="address_add"),   
path("orders/<str:slug>/",views.order_track,name="order_track"),        
path("order/user/<str:slug>/",views.manage_order,name="manage_order"),   
path("canceled/order/<str:slug>/",views.canceled_order,name="canceled_order"),         
path("FAQ/",views.faq,name="faq"),         
path("about/",views.about,name="about"),            
path("contact/",views.contact,name="contact"),            

## news
path("news/",views.news,name="news"),            

## filter_delete    
path("filter/color",views.color_filter_delete,name="color_delete"),
path("filter/price",views.price_filter_delete,name="price_delete"),
path("filter/ship",views.ship_filter_delete,name="ship_delete"),
path("filter/size",views.size_filter_delete,name="size_delete"),
path("filter/category",views.category_filter_delete,name="category_delete"),
path("filter/manufacrurer",views.manu_filter_delete,name="manu_delete"),
path("filter/rate",views.rate_filter_delete,name="rate_delete"),

# Cart
path("add-to-cart/<str:id>/",views.add_to_cart,name="cart_add"),
path("remove-from-cart/<str:id>/",views.remove_from_cart,name="cart_remove"),
path("whislist-add/<str:id>/",views.wishlist_add,name="wishlist_add"),
path("whislist-remove/<str:id>/",views.wishlist_remove,name="wishlist_remove"),
path("quantity/add/<str:id>/",views.quantity_add,name="quantity_add"),
path("cart/clear/",views.cart_clear,name="cart_clear"),
path("whislist-list-remove/",views.wishlist_list_remove,name="wishlist_list_remove"),
path("make_primary/",views.make_primary,name="make_primary"),
path("make-new-address/",views.make_new_address,name="make_new_address"),
path("address_edit/<str:id>/",views.address_edit,name="address_edit"),  
path("make-payment-option/",views.make_payment_option,name="make_payment_option"),
path("quantity_add/<str:id>/",views.cart_quantity_add,name="cart_quantity_add"),
path("quantity_remove/<str:id>/",views.cart_quantity_remove,name="cart_quantity_remove"),
path("coupon/",views.coupon,name="coupon"),
### PAYMNETS

path("create/<str:id>/",views.create,name="create"),

#       Dashboard              
path("dashboard/",views.dashboard,name="dashboard"),
path("dashboard/products/add",views.add_products,name="products_add"),
path("dashboard/products/modify/<str:id>/",views.modify_product,name="products_modify"),
path("dashboard/products/delete_product/<str:id>/",views.delete_product,name="product_delete"),
path("dashboard/deals/",views.deals,name="deals"),
path("dashboard/deals/add/",views.deals_add,name="deals_add"),
path("dashboard/deals/delete/<str:id>/",views.deals_delete,name="deals_delete"),
path("dashboard/category/",views.category_dash,name="category"),
path("dashboard/category/add/",views.category_add,name="category_add"),
path("dashboard/category/delete/<str:id>/",views.category_delete,name="category_delete"),
path("dashboard/branch/",views.branch,name="branch"),
path("dashboard/branch/add/",views.branch_add,name="branch_add"),
path("dashboard/branch/delete/<str:id>/",views.branch_delete,name="branch_delete"),
path("dashboard/manu/",views.manu,name="manu"),
path("dashboard/manu/add/",views.manu_add,name="manu_add"),
path("dashboard/manu/delete/<str:id>/",views.manu_delete,name="manu_delete"),


]             
         
 