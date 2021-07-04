from django.contrib import admin
from .models import * 
# Register your models here.

class OrderStatus(admin.ModelAdmin):
    list_display=["user","ordered","delivered","device"]

admin.site.register(Branch)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Manufacturer)
admin.site.register(Size)
admin.site.register(Product)
admin.site.register(Images)
admin.site.register(Filter)
admin.site.register(Product_Cart,OrderStatus)
admin.site.register(Cart,OrderStatus)     
admin.site.register(Wishlist)     
