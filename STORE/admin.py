from django.contrib import admin
from .models import * 
# Register your models here.

class OrderStatus(admin.ModelAdmin):
    list_display=["user","ordered","delivered","device","id"]
class FilterAdmin(admin.ModelAdmin):
    list_display=["user","device"]
class ProductAdmin(admin.ModelAdmin):
    list_display=["products","user","ordered","delivered","device"]
class WishlsitAdmin(admin.ModelAdmin):
    list_display=["user","device","id"]
class AddressAdmin(admin.ModelAdmin):
    list_display=["profile","primary"]
class DealAdmin(admin.ModelAdmin):
    list_display=["id","expired"]
admin.site.register(Branch)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Manufacturer)
admin.site.register(Size)
admin.site.register(Product)
admin.site.register(Images)
admin.site.register(Filter,FilterAdmin)
admin.site.register(Product_Cart,ProductAdmin)
admin.site.register(Cart,OrderStatus)     
admin.site.register(Wishlist,WishlsitAdmin)     
admin.site.register(Rate)     
admin.site.register(Rate_Details)     
admin.site.register(Order,OrderStatus)     
# admin.site.register(Delivery_Info)        
admin.site.register(Profile)     
admin.site.register(Address,AddressAdmin)     
admin.site.register(FAQ)     
admin.site.register(Contact)        
admin.site.register(NewsLetter)     
admin.site.register(Deals,DealAdmin)     
admin.site.register(Coupon)
admin.site.register(Shipping)
admin.site.register(Blog_Comments)     
admin.site.register(Blogs)
admin.site.register(Blog_Images)
admin.site.register(Blog_Category)

