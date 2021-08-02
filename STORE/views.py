from django.shortcuts import render,redirect,reverse
from .models import *
from .forms import *
from .filters import *
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.conf import settings
# import login_required()
# Create your views here.    
from datetime import date   
import time
from django.utils import timezone
from django.utils.timezone import get_current_timezone
def home(request):
    trend=Product.objects.order_by("-stars")[0:12]
    arrivals=Product.objects.order_by("-id")[0:8]
    category=Category.objects.all()   
    most_buy=Product.objects.order_by("-most_buy")[0:3]
    for i in Deals.objects.filter(expired=False):
        if i.expire_date.date() < date.today() or i.expire_date.date() == date.today():
            i.expired=True
            i.save()   
    deal=Deals.objects.filter(expired=False) 

    context={"deals":deal,"paid":most_buy,"trend":trend,"arrivals":arrivals,"category":category}
    return render(request,"home.html",context) 
def products(request):
    selected=0 # this is for sortings products 
    paginate=0  #this is for paginat page number 
    free=request.POST.get("free")
    # size=request.POST.get("size")
    price_1=request.POST.get("price_1")
    price_2=request.POST.get("price_2")
    rate=request.POST.get("rate")
    category=Category.objects.all()
    # color=request.POST.get("color")
    # manu=request.POST.get("manu")  
    paginat=request.POST.get("paginat")
    select_filter=request.POST.get("select_filter")
    # product=Product.objects.order_by("-id")   
    if request.user.is_authenticated:
        repeat_user=Filter.objects.filter(user=request.user)   
        if len(repeat_user) != 1:
            for i in repeat_user[1:]:
                i.delete()           
        filter_user,creatde=Filter.objects.get_or_create(user=request.user)
        # cart,created=Cart.pbjects
        # print(carts)   
        try:      
            device=request.COOKIES["device"]
            filter_user.device=device
            filter_user.save()
           
            if len(Filter.objects.filter(device=device)) != 1:
                for i in Filter.objects.filter(device=device):
                    i.delete()
            for i in Filter.objects.filter(user=None,device=device):
                i.user=request.user
                i.save()
        except:
            pass
            
              
        if free:
            try:
                filter_user.shipping=True
                filter_user.save()
            except:
                messages.error(request,"sorry,invalid value")
                pass

        if price_1 and price_2:
            try:
                filter_user.price_1=price_1
                filter_user.price_2=price_2
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
            
        if rate:          
            try:
                filter_user.rating=rate
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
        if select_filter:
            try:
                filter_user.sort= select_filter
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
        
        if paginat:
            try:
                filter_user.show= paginat
                filter_user.save() 
            except:
                messages.error(request,"sorry.invalid value")
                pass
        if filter_user.category == None and filter_user.color == None and filter_user.size == None and  filter_user.manufacturer == None and filter_user.rating == None and filter_user.price_1 == None and filter_user.shipping ==False :
            if filter_user.sort == 0 or filter_user.sort == 1 or filter_user.sort == "1":
                product=Product.objects.order_by("-id")   
                selected=1      
            if filter_user.sort == 2 or filter_user.sort == "2": 
                product=Product.objects.order_by("id")
                selected=2  
            
            if filter_user.sort == 5 or filter_user.sort == "5":
                product=Product.objects.order_by("price")
                selected=5  
                
            if filter_user.sort == 6 or filter_user.sort == "6":
                product=Product.objects.order_by("-price") 
                selected=6       
        else:
            filters={}
            price_range=(filter_user.price_1,filter_user.price_2)
            stars_range=(filter_user.rating,float(filter_user.rating) + float(0.5))
            lists={"stars__range":stars_range,"price__range":price_range,"free_shipping":filter_user.shipping}
            # lists={}
   
            for i in lists:
                b=lists[i]
                if  b != None and b != (None,None) and b != (0.0,0.5):     
                    
                    filters[i]=b
               
            if filter_user.sort == 0 or filter_user.sort == 1 or filter_user.sort == "1":
                product=Product.objects.filter(**filters).order_by("-id")   
                selected=1      
            elif filter_user.sort == 2 or filter_user.sort == "2": 
        
                product=Product.objects.filter(**filters).order_by("id")
                selected=2 
            elif filter_user.sort == 5 or filter_user.sort == "5":
                product=Product.objects.filter(**filters).order_by("price")
                selected=5  
            elif filter_user.sort == 6 or filter_user.sort == "6":
                product=Product.objects.filter(**filters).order_by("-price") 
                selected=6
        # s=Cart.objects.get(user=request.user,ordered=True,delivered=False)

    else:  
        try:   
            device=request.COOKIES["device"] 
        except:     
            device=[]       
            pass        
        repeat_anonymous=Filter.objects.filter(device=device)
        if  len(repeat_anonymous) != 1:    
            for i in repeat_anonymous:   
                i.delete()
    
        # same=Product_Cart.objects.filter(device=device,ordered=True,delivered=False) 
        filter_user,created=Filter.objects.get_or_create(device=device)
        if free:
            try:
                filter_user.shipping=True
                filter_user.save()
            except:
                messages.error(request,"sorry,invalid value")
                pass
        # if size:
        #     try:
        #         filter_user.size_id=size
        #         filter_user.save()    
        #     except:
        #         messages.error(request,"sorry,invalid value")
        #         pass

        if price_1 and price_2:
            try:
                filter_user.price_1=price_1
                filter_user.price_2=price_2
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
            
        if rate:          
            try:
                filter_user.rating=rate
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
        # if color:                        
        #     try:
        #         filter_user.color_id=color 
        #         filter_user.save()
        #     except:
        #         messages.error(request,"sorry.invalid value")
        #         pass
        # if manu:    
        #     try:
        #         filter_user.manufacturer_id=manu      
        #         filter_user.save()
        #     except:
        #         messages.error(request,"sorry.invalid value")
        #         pass
        if select_filter:
            try:
                filter_user.sort= select_filter
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
        
        if paginat:
            try:
                filter_user.show= paginat
                filter_user.save() 
            except:
                messages.error(request,"sorry.invalid value")
                pass
        if filter_user.category == None and filter_user.color == None and filter_user.size == None and  filter_user.manufacturer == None and filter_user.rating == None and filter_user.price_1 == None and filter_user.shipping ==False :
            if filter_user.sort == 0 or filter_user.sort == 1 or filter_user.sort == "1" :
              
                selected=1
                product=Product.objects.order_by("-id")  
            if filter_user.sort == 2 or filter_user.sort == "2":
                
                selected=2      
                product=Product.objects.order_by("id")   
            if filter_user.sort == 5 or filter_user.sort == "5":
                 
                selected=5
                product=Product.objects.order_by("price")  
            if filter_user.sort == 6 or filter_user.sort == "6":
            
                selected=6
                product=Product.objects.order_by("-price")    
        else:      
            filters={}
            price_range=(filter_user.price_1,filter_user.price_2)
            stars_range=(filter_user.rating,float(filter_user.rating) + float(0.5))
            lists={"stars__range":stars_range,"price__range":price_range,"free_shipping":filter_user.shipping}
            for i in lists:
                b=lists[i]
                if  b != None and b != (None,None) and b != (0.0,0.5):     
                    print(i,b)
                    filters[i]=b
            if filter_user.sort == 0 or filter_user.sort == 1 or filter_user.sort == "1":
                product=Product.objects.filter(**filters).order_by("-id")   
                selected=1         
            elif filter_user.sort == 2 or filter_user.sort == "2": 
        
                product=Product.objects.filter(**filters).order_by("id")
                selected=2   
            elif filter_user.sort == 5 or filter_user.sort == "5":
                product=Product.objects.filter(**filters).order_by("price")
                selected=5  
            elif filter_user.sort == 6 or filter_user.sort == "6":
                product=Product.objects.filter(**filters).order_by("-price") 
                selected=6
    try:
        paginator = Paginator(product, filter_user.show) # Show requested products per page.    
        paginated=int(filter_user.show)
    except:
        paginator = Paginator(product,8 ) # Show 8 products per page.  
        paginated=8
    page_number = request.GET.get('page')    
    page_obj = paginator.get_page(page_number)                        
    context={"category":category,"my_filter":filter_user,"products":page_obj,"paginated":paginated,"selected":selected,"show":paginate}
    return render(request,"products.html",context)
   
def this_product(request,id):

    product=get_object_or_404(Product,id=id)
    same=Product.objects.filter(branch=product.branch,name__icontains=product.name).order_by("-id")[0:4]
    reviews=Rate.objects.filter(product__id=product.id) #specific rate for particular product
    form=RateForm(request.POST or None)
    comments=request.POST.get("comments")
    if comments:
        print(comments)
        if comments == 1:    
            details=Rate_Details.objects.filter(rate_id__in=reviews,product=product).order_by("-stars","-id")   #details for this rate
        if comments == 2:
            details=Rate_Details.objects.filter(rate_id__in=reviews,product=product).order_by("stars","-id")   #details for this rate
    else:
        details=Rate_Details.objects.filter(rate_id__in=reviews,product=product).order_by("-stars","-id")   #details for this rate
  
    if form.is_valid():            
        instance=form.save(commit=False)
        review=form.cleaned_data.get("review")
        stars=form.cleaned_data.get("stars")
        if not 1 <= float(stars) <= 5:
            messages.error(request,"value is not correct")
            return redirect(reverse("home:this_product",kwargs={"id":product.id}))
        if request.user.is_authenticated:
            try:
                this_rate=Rate.objects.get(user=request.user)
                this_rate.product.add(product)
                this_rate.save()
                my_rate=Rate_Details.objects.create(rate_id=this_rate.id,product=product,review=review,stars=stars)
                product.stars +=float(stars)
                product.save()
                print("added")    
            except:
                new_rate=Rate.objects.create(user=request.user)   
                new_rate.product.add(product)
                new_rate.save()    
                my_rate=Rate_Details.objects.create(rate_id=new_rate.id,product=product,review=review,stars=stars)
                product.stars +=float(stars)
                product.save()
                print("created")    
        else:
            messages.error(request,"you should login first")
            return redirect(reverse("account_login"))    

    context={"product":product,"same":same,"form":form,"reviews":reviews,"details":details}
    return render(request,"this_product.html",context)

def cart(request):
    cities=City.objects.all()
    if request.user.is_authenticated:
        repeat_product=Product_Cart.objects.filter(user=request.user,ordered=True,delivered=False)
        repeat_cart=Cart.objects.filter(user=request.user,ordered=True,delivered=False)
        # order=
        if len(repeat_cart) != 1:    
            for i in repeat_cart:
                i.delete()
        try:
            device=request.COOKIES['device']
            repeat_cart=Cart.objects.filter(device=device,ordered=True,delivered=False)
            if len(repeat_cart) != 1:
                for i in repeat_cart:
                    i.delete()
            if Cart.objects.filter(user=request.user,ordered=True,delivered=False).exists():
                cart=Cart.objects.get(user=request.user,ordered=True,delivered=False)
                cart.device=device
                cart.save()
                print("saved device")
            if Cart.objects.filter(device=device,user=None,ordered=False,delivered=True).exists():
                cart=Cart.objects.get(device=device,user=None,ordered=True,delivered=False)
                cart.user=request.user
                cart.save()
            repeat_device_product=Product_Cart.objects.filter(device=device,user=None,ordered=True,delivered=False)
            for i in repeat_device_product:
                i.user=request.user
                i.save()
            for i in repeat_product:
                i.device=device
                i.save()
            cart,created=Cart.objects.get_or_create(user=request.user,device=device,ordered=True,delivered=False)
            if len(cart.products.all()) == 0:
                return redirect(reverse("home:empty"))
        except:
            cart,created=Cart.objects.get_or_create(user=request.user,ordered=True,delivered=False)
            if len(cart.products.all()) == 0:
                return redirect(reverse("home:empty"))
            pass 
    else:    
        try:        
            device=request.COOKIES["device"]     
            repeat_cart=Cart.objects.filter(device=device,ordered=True,delivered=False)
            if len(repeat_cart) !=1:
                for i in repeat_cart:
                    i.delete()
            cart,created=Cart.objects.get_or_create(device=device,ordered=True,delivered=False)
            if len(cart.products.all()) == 0:
                return redirect(reverse("home:empty"))
        except:    
            return redirect(reverse("home:empty"))
            pass
    context={"cities":cities}
    return render(request,"cart.html",context)
  
def empty(request):
      
    return render(request,"empty.html")   

  
def cart_clear(request):
    if request.user.is_authenticated:
        repeat_cart=Cart.objects.filter(user=request.user,ordered=True,delivered=False)
        if len(repeat_cart) != 1:
            for i in repeat_cart:
                i.delete()
        cart=Cart.objects.get(user=request.user,ordered=True,delivered=False)
        for i in cart.products.all():    
            i.delete()
    else:
        device=request.COOKIES["device"]
        repeat_cart=Cart.objects.filter(device=device,ordered=True,delivered=False)
        if len(repeat_cart) != 1:
            for i in repeat_cart:
                i.delete()
        cart=Cart.objects.get(device=device,ordered=True,delivered=False)
        for i in cart.products.all():    
            i.delete()
    return redirect(reverse("home:cart"))

def add_to_cart(request,id):
    device=request.COOKIES["device"]
    product=get_object_or_404(Product,id=id)
    if request.user.is_authenticated:
        repeat_product=Product_Cart.objects.filter(user=request.user,delivered=False)
        for i in repeat_product:
            if i.device != device:
                i.device=device
                i.save()
                print("reapeat product")
        repeat_cart=Cart.objects.filter(user=request.user,ordered=True,delivered=False)
        for i in repeat_cart:
            if i.device != device:
                i.device=device
                i.save()
                print("repeat cart")
        repeat_cart_device=Cart.objects.filter(device=device,ordered=True,delivered=False)
        if len(repeat_cart_device)  != 1:
            for i in repeat_cart:
                i.delete()

        product_cart,created=Product_Cart.objects.get_or_create(products=product,user=request.user,delivered=False)
        product_cart.device=device
        product_cart.save()
        print("prodcut_cart authenticated")
        # for i in Cart.objects.filter(user=request.user,ordered=True,delivered=False):
        #     if i.device != device:
        #         i.device=device
        #         i.save() 
        cart,created=Cart.objects.get_or_create(user=request.user,ordered=True,delivered=False,device=device)
        if product_cart in cart.products.all():
            messages.error(request,"this item is in your cart")
        else:
            cart.products.add(product_cart)   
            cart.device=device
            product_cart.ordered=True     
            product_cart.save()    
            cart.save()
            print("cart authenticated")         
            messages.success(request,"Item Added Successfully")    
    else:
        device=request.COOKIES["device"]
        repeat_product=Product_Cart.objects.filter(device=device,delivered=False)
        repeat_cart=Cart.objects.filter(device=device,ordered=True,delivered=False)
        if len(repeat_cart) != 1:
            for i in repeat_cart:
                for b in i.products.all():
                    b.delete()
                i.delete()

            # for i in    
            
        product_cart,created=Product_Cart.objects.get_or_create(products=product,device=device,delivered=False)
        print("prodcut_cart anonymous")
        cart,created=Cart.objects.get_or_create(device=device,ordered=True,delivered=False)
        if product_cart in cart.products.all():
            messages.error(request,"this item is in your cart")
        else:
            cart.products.add(product_cart)  
            product_cart.ordered=True     
            product_cart.save()    
            cart.save()
            print("cart anonymous")         
            messages.success(request,"Item Added Successfully") 
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    
        # product_cart.

def cart_quantity_add(request,id):
    product_cart=Product_Cart.objects.get(id=id)
    if product_cart.quantity >= 10:
        messages.error(request,"you have reached the maximum quantity")
        return redirect(reverse("home:cart"))

    product_cart.quantity +=1
    product_cart.save()
    return redirect(reverse("home:cart"))
    
def cart_quantity_remove(request,id):
    product_cart=Product_Cart.objects.get(id=id)
    product_cart.quantity -=1
    product_cart.save()
    if product_cart.quantity <= 0:
        product_cart.delete()
    return redirect(reverse("home:cart"))
    


def remove_from_cart(request,id):
    device=request.COOKIES["device"]
    product=get_object_or_404(Product,id=id)
    if request.user.is_authenticated:
        repeat_product=Product_Cart.objects.get(user=request.user,ordered=True,delivered=False,products_id=product.id)
        repeat_product.delete()
        print("delted")
        # repeat_cart=Cart.objects.get(user=request.user,ordered=True,delivered=False)
        # repeat_cart.products.remove(product)
        messages.success(request,"Item removed Successfully")    
    else:
        repeat_product=Product_Cart.objects.get(device=device,ordered=True,delivered=False,products_id=product.id)
        repeat_product.delete()
        print("delted")
        # repeat_cart=Cart.objects.get(user=request.user,ordered=True,delivered=False)
        # repeat_cart.products.remove(product)
        messages.success(request,"Item removed Successfully")        
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def quantity_add(request,id):
    my_quantity=request.POST.get("quantity")          
    device=request.COOKIES["device"]
    color=request.POST.get("color")
    size=request.POST.get("size")
    if not Color.objects.filter(id=int(color)).exists() or not Size.objects.filter(id=int(size)).exists() or float(my_quantity) <= 0:
        messages.error(request,"invalid values")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    if request.user.is_authenticated:
        repeat_product=Product_Cart.objects.filter(user=request.user,delivered=False)
        for i in repeat_product:
            if i.device != device:
                i.device=device
                i.save()
                print("reapeat product")

        repeat_cart=Cart.objects.filter(user=request.user,ordered=True,delivered=False)
        for i in repeat_cart:
            if i.device != device:
                i.device=device
                i.save()
                print("repeat cart")

        cart=Cart.objects.filter(user=request.user,ordered=True,delivered=False)
        if cart.exists():
            if len(cart) != 1:
                for i in cart:
                    i.delete()
            my_cart=Cart.objects.get(user=request.user,ordered=True,delivered=False)
            try:
                product_cart= Product_Cart.objects.get(user=request.user,ordered=True,delivered=False,products_id=id)
                product_cart.device=device
                product_cart.save()
                if color:
                    product_cart.color_id=color
                    product_cart.save()
                if size:
                    product_cart.size_id=size
                    product_cart.save()
                for i in my_cart.products.all():
                    if i.id == product_cart.id:
                        if  i.quantity >= 10:
                            messages.error(request,"you have reached maximum quantity")
                            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                        i.quantity +=int(my_quantity)
                        i.device=device
                        i.save()
                        print("saved")   
            except:   
                new_product=Product_Cart.objects.create(user=request.user,products_id=id,ordered=True,delivered=False,device=device,quantity=int(my_quantity))
                if color:
                    new_product.color_id=color
                    new_product.save()
                if size:       
                    new_product.size_id=size
                    new_product.save()                         
                my_cart.products.add(new_product)
                my_cart.save() 
                print("cart saved")       
        else:  
            product=Product_Cart.objects.create(user=request.user,ordered=True,quantity=int(my_quantity),products_id=id,delivered=False,device=device,size_id=size) 
            if color:
                product.color_id=color
                product.save()
            if size:
                product.size_id=size
                product.save()
            cart=Cart.objects.create(user=request.user,ordered=True,delivered=False,device=device)
            cart.products.add(product)
            print("cart created")  
    else:
        # repeat_product=Product_Cart.objects.filter(device=device,delivered=False)
        cart=Cart.objects.filter(device=device,ordered=True,delivered=False)
        if len(cart) != 1: 
            for i in cart:
                i.products.delete()
                i.delete()
                print("deleted")
        if cart.exists():
            my_cart=Cart.objects.get(device=device,ordered=True,delivered=False)
            try:
                product_cart= Product_Cart.objects.get(device=device,ordered=True,delivered=False,products_id=id)
                if color:
                    product_cart.color_id=color
                if size:
                    product_cart.size_id=size
                    product_cart.save()
                for i in my_cart.products.all():
                    if i.id == product_cart.id:
                        if  i.quantity >= 10:
                            messages.error(request,"you have reached maximum quantity")
                            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
                        i.quantity +=int(my_quantity)
                        i.device=device
                        i.save()
                        print("saved")   
            except:
                new_product=Product_Cart.objects.create(products_id=id,ordered=True,delivered=False,device=device,quantity=int(my_quantity))
                if color:
                    new_product.color_id=color
                    new_product.save()
                if size:
                    new_product.size_id=size
                    new_product.save()
                my_cart.products.add(new_product)
                my_cart.save() 
                print("cart saved")       
        else:  
            product=Product_Cart.objects.create(ordered=True,quantity=int(my_quantity),products_id=id,delivered=False,device=device) 
            if color:
                product.color_id=color
                product.save()
            if size:
                product.size_id=size    
                product.save()      
            cart=Cart.objects.create(user=request.user,ordered=True,delivered=False,device=device)
            cart.products.add(product)
            print("cart created")  
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
          
def make_primary(request):
    profile=Profile.objects.get(user=request.user)
    address=Address.objects.filter(profile=profile)
    order=Order.objects.get(user=request.user,ordered=True,delivered=False)
    value=request.POST.get("default-address")
    try:      
        print(int(value))
        for i in address:    
            i.primary =False
            i.save()

            if i.id == int(value):    
                i.primary=True     
                i.save()
                order.address=i
                order.save()
                print("asdasdasd")
        
    except:
        pass
  
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
   
       
def make_new_address(request):
    profile=Profile.objects.get(user=request.user)
    phone=request.POST.get("phone")
    street=request.POST.get("street")
    city=request.POST.get("city")
    country=request.POST.get("country")
    zip=request.POST.get("zip")                      
    if len(Address.objects.filter(profile=profile)) >= 3:   
        messages.error(request,"sorry,you should have 3 Address only")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        try:
            Address.objects.create(profile=profile,phone=phone,street=street,country=country,city_id=city,zip=zip)
        except:  
            messages.error(request,"sorry, invalid data")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def make_payment_option(request):
    profile=Profile.objects.get(user=request.user)
    payment=request.POST.get("payment")
    order=Order.objects.get(user=request.user,ordered=True,delivered=False)
    try:
        if payment != None:
            order.payments=str(payment)
            order.save()  
            if order.payments == None or order.address == None or order.cart == None:
                print("none order")   
                messages.error(request,"please complete your order information")
                return redirect(reverse("home:order",kwargs={"id":order.cart.cart.id}))
        else:
            print(payment)
            messages.error(request,"sorry, invalid payment option")
            return redirect(reverse("home:order",kwargs={"id":order.cart.cart.id}))
    except:
       
        messages.error(request,"sorry,invalid payment option")
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


### payment views

from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalcheckoutsdk.orders import OrdersCaptureRequest
from paypalcheckoutsdk.core import SandboxEnvironment,PayPalHttpClient
CLIENT_ID="AUVCElDtljJUDVWukP9yrdedNic0J1B1XY1MtNfPhqxQU47F1F1A7C6ixKabvUCRZCTpkFihHBaTPR-F"
CLIENT_SECRET="ENepKuG3KheVNsthJjDS7B2amndWXWwaAQz3PJj8Ddi6O-QFQenD9frvveoUdGLrUdJUQ0DlzVap_b9Z"
# @login_required()
def create(request,id):
    if request.method =="POST":
        environment = SandboxEnvironment(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        client = PayPalHttpClient(environment)

        order= Order.objects.get(user=request.user,ordered=True,delivered=False)
        create_order = OrdersCreateRequest()
        #order            
        create_order.request_body (
            
            {
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": "USD",
                            "value": order.price,
                            "breakdown": {
                                "item_total": {
                                    "currency_code": "USD",
                                    "value":  order.price
                                }
                                },
                            },                               


                    }
                ],      
                

            }     
        )
       
        # print()
        response = client.execute(create_order)
        data = response.result.__dict__['_dict']      
        return JsonResponse(data)
    else:
        return JsonResponse({'details': "invalide request"})


def coupon(request):
    if request.user.is_authenticated:
        order=Order.objects.get(user=request.user,ordered=True,delivered=False)
        profile=Profile.objects.get(user=request.user)
        my_coupon=request.POST.get("coupon")
        try:
            coupon=Coupon.objects.get(coupon__iexact=my_coupon)
           
            if order.coupon == None:
                print(order.coupon)
                total=order.price - (coupon.value/100)*order.price
                order.price=total
                order.coupon=coupon
                order.save()  
                print("discount") 
            else:
                messages.error(request,"sorry you already have a coupon")
                return redirect(reverse("home:order",kwargs={"id":order.cart.id}))
        except:
    
            pass
    else:
        pass
    return redirect(reverse("home:order",kwargs={"id":order.cart.id}))

def order(request,id):
    cities=City.objects.all()
    if request.user.is_authenticated:
        profile=get_object_or_404(Profile,user=request.user)
        repeat_order=Order.objects.filter(user=request.user,ordered=True,delivered=False)
        if len(repeat_order) != 1:
            for i in repeat_order:
                i.delete()
        repeat_cart=Cart.objects.filter(user=request.user,ordered=True,delivered=False)
        if len(repeat_cart) != 1:
            for i in repeat_cart:     
                i.delete()
        cart=get_object_or_404(Cart,id=id) 
        if cart.order_product_length() == 0:     
            messages.error(request,"you dont have products in your cart")
            return redirect(reverse("home:cart"))
        try:
            my_address=Address.objects.get(profile=profile,primary=True)
        except:
            my_address=[]
            pass
        all_address=Address.objects.filter(profile=profile)          
        order,created=Order.objects.get_or_create(user=request.user,ordered=True,cart=cart,delivered=False)
        if Address.objects.filter(profile=profile,primary=True).exists():
            this_address=Address.objects.get(profile=profile,primary=True)
            order.address=this_address
            order.save()
        if order.price == 0: 
            order.price=cart.total_price()    
            order.save()         
        try:
            device=request.COOKIES["device"]
            order.device=device
            order.save()      
        except:
            pass 
        if request.method == 'POST':
            notes=request.POST.get("note") 
            phone=request.POST.get("phone")
            street=request.POST.get("street")
            city=request.POST.get("city")
            country=request.POST.get("country")
            zip=request.POST.get("zip")
            default=request.POST.get("default")
            primary=request.POST.get("primary")
            print(default)                      
            if len(Address.objects.filter(profile=profile)) >= 3:
                messages.error(request,"sorry,you should have 3 Address only")
                return redirect(reverse("home:order",kwargs={"id":cart.id}))       
            if default == None:
                address=Address.objects.create(profile=profile,phone=phone,street=street,country=country,city_id=city,zip=zip)              
                order.address= address
                order.save()
                if primary == "on":
                    for i in Address.objects.filter(profile=profile):
                        i.primary=False
                        i.save()
                    address.primary =True
                    address.save()

                if notes:
                    order.notes=notes                    
                    order.save()

            elif default == "on":
                try:
                    address=Address.objects.get(profile=profile,primary=True)
                    order.address=address
                    order.save()
                    if notes:     
                        order.notes=notes
                        order.save()  
                except:
                    messages.error(request,"you dont have a primary address")
                    return redirect(reverse("home:order",kwargs={"id":cart.id}))
            

    else:               
        messages.error(request,"you must login to place your order")
        return redirect(reverse("account_login"))
    context={"order":order,"cities":cities,"my_address":my_address,"all":all_address}
    return render(request,"checkout.html",context)
def profile(request,slug):    
    if request.user.is_authenticated:
        profile=Profile.objects.get(user=request.user)
        all_order=Order.objects.filter(user=request.user,ordered=True,delivered=True)
        repeat_order=Order.objects.filter(user=request.user,ordered=True,delivered=False)
        if len(repeat_order) != 1:
            for i in repeat_order:
                i.delete()
        order=Order.objects.filter(ordered=True,delivered=True,user=request.user).exclude(statue="canceled").count()
        canceled_order=Order.objects.filter(ordered=True,delivered=True,user=request.user,statue="canceled").count()
        try:
            info=Address.objects.get(profile=profile,primary=True)
        except:
            info={}
 
    else:    
        messages.error(request,"please login First....")
        return redirect(reverse("account_login"))

    context={"profile":profile,"all":all_order,"order":order,"canceled":canceled_order,"info":info}
    return render(request,"profile.html",context)

def profile_account(request,slug):   
    if request.user.is_authenticated:
        profile=Profile.objects.get(user=request.user)
        order=Order.objects.filter(ordered=True,delivered=True,user=request.user).exclude(statue="canceled").count()
        canceled_order=Order.objects.filter(ordered=True,delivered=True,user=request.user,statue="canceled").count()
    else:
        messages.error(request,"please login First....")
        return redirect(reverse("account_login"))

    context={"profile":profile,"order":order,"canceled":canceled_order}
    return render(request,"profile_account.html",context)

def profile_edit(request,slug):   
    if request.user.is_authenticated:
        profile=Profile.objects.get(user=request.user)
        form=ProfileForm(request.POST or None,instance=profile)
        order=Order.objects.filter(ordered=True,delivered=True,user=request.user).exclude(statue="canceled").count()
        canceled_order=Order.objects.filter(ordered=True,delivered=True,user=request.user,statue="canceled").count()
        month=request.POST.get("birthday_month")
        year=request.POST.get("birthday_year")
        day=request.POST.get("birthday_day")     
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        gender=request.POST.get("gender")
        phone=request.POST.get("phone")
        
        date=f"{year}-{month}-{day}"
        if request.method == 'POST':   
            try:                   
                if gender != "Male" and gender != "Female":
                    print(gender)  
                    messages.error(request,"sorry,invalid data")
                    return redirect(reverse("home:profile_edit",kwargs={"slug":profile.user}))
                profile.birthday=date  
                profile.user.first_name=first_name
                profile.user.last_name=last_name
                profile.gender=gender
                profile.phone=phone
                profile.save()
                print("done")
            except:
                messages.error(request,"sorry,invalid data")
                return redirect(reverse("home:profile_edit",kwargs={"slug":profile.user}))
    else:
        messages.error(request,"please login First....")
        return redirect(reverse("account_login"))

    context={"profile":profile,"order":order,"canceled":canceled_order,"form":form}
    return render(request,"profile_edit.html",context)

 
def address(request,slug):
    if request.user.is_authenticated:
        city=City.objects.all()
        profile=Profile.objects.get(user=request.user)
        info=Address.objects.filter(profile=profile)
        order=Order.objects.filter(ordered=True,delivered=True,user=request.user).exclude(statue="canceled").count()
        canceled_order=Order.objects.filter(ordered=True,delivered=True,user=request.user,statue="canceled").count()

    else:        
        messages.error(request,"please login First....")
        return redirect(reverse("account_login"))

    context={"profile":profile,"cities":city,"info":info,"canceled":canceled_order,"order":order}
    return render(request,"address_book.html",context)
def address_add(request,slug):    
    if request.user.is_authenticated:
        cities=City.objects.all()
        profile=Profile.objects.get(user=request.user)
        info=Address.objects.filter(profile=profile)
        order=Order.objects.filter(ordered=True,delivered=True,user=request.user).exclude(statue="canceled").count()
        canceled_order=Order.objects.filter(ordered=True,delivered=True,user=request.user,statue="canceled").count()
        if len(info) >= 3:
                return redirect(reverse("home:address",kwargs={"slug":profile.user}))
        else:
            if request.method == 'POST':
                phone=request.POST.get("phone")
                street=request.POST.get("street")
                state=request.POST.get("state")
                city=request.POST.get("city")
                zip=request.POST.get("zip")
                try:
                    address=Address.objects.create(profile=profile,phone=phone,street=street,country=state,city_id=city,zip=zip)
                    if len(Address.objects.filter(profile=profile)) ==1:
                        address.primary=True
                        address.save()
                    messages.success(request,"Address Added successfully")
                    return redirect(reverse("home:address_add",kwargs={"slug":profile.user}))
                except:
                    messages.error(request,"invalid data")
                    return redirect(reverse("home:address_add",kwargs={"slug":profile.user}))


    else:
        messages.error(request,"please login First....")
        return redirect(reverse("account_login"))

    context={"profile":profile,"cities":cities,"canceled":canceled_order,"order":order,"info":info}
    return render(request,"address_add.html",context)

def address_edit(request,id):
    address=Address.objects.get(profile__user=request.user,id=id)
    form=AddressEdit(request.POST or None,instance=address)
    if form.is_valid():
        form.save()
    else:
        messages.error(request,"invalid data")
    return redirect(reverse("home:address",kwargs={"slug":request.user}))


def order_track(request,slug):
    if request.user.is_authenticated:
        orders=Order.objects.filter(user=request.user)
        profile=Profile.objects.get(user=request.user)
        order=Order.objects.filter(ordered=True,delivered=True,user=request.user).exclude(statue="canceled").count()
        canceled_order=Order.objects.filter(ordered=True,delivered=True,user=request.user,statue="canceled").count()
        track=request.POST.get("track")
        my_order=Order.objects.filter(user=request.user,track_number=track) #user=request.user,ordered=True,delivered=True,
        # if request.is_ajax():
        #     print("ajax")
        #     data=list(orders.values())  
        #     return JsonResponse(data,safe=False)
            # return   
    else:        
        messages.error(request,"please login First....")
        return redirect(reverse("account_login"))

    context={"profile":profile,"order":order,"canceled":canceled_order,"orders":my_order}

    return render(request,"order_track.html",context)

def manage_order(request,slug):
    if request.user.is_authenticated:
        profile,created=Profile.objects.get_or_create(user=request.user)
        try:
            my_order=Order.objects.get(user=request.user,ordered=True,delivered=True) #user=request.user,ordered=True,delivered=True,
        except:
            return redirect(reverse("home:empty"))    
    else:     
        messages.error(request,"please login First....")
        return redirect(reverse("account_login"))
    context={"order":my_order}
    return render(request,'manage_order.html',context)
def canceled_order(request,slug):
    if request.user.is_authenticated:
        profile=Profile.objects.get(user=request.user)
        my_order=Order.objects.filter(user=request.user,ordered=True,delivered=True,statue="canceled") #user=request.user,ordered=True,delivered=True,
        order=Order.objects.filter(ordered=True,delivered=True,user=request.user).exclude(statue="canceled").count()
        canceled_order=Order.objects.filter(ordered=True,delivered=True,user=request.user,statue="canceled").count()
    else:     
        messages.error(request,"please login First....")
        return redirect(reverse("account_login"))
    context={"my_order":my_order,"order":order,"canceled":canceled_order}
    return render(request,'canceled_order.html',context)

def rate_filter_delete(request):
    if request.user.is_authenticated:     
        filter=Filter.objects.get(user=request.user)   
        filter.rating = 0
        filter.save()
    else:
        device=request.COOKIES["device"]
        filter=Filter.objects.get(device=device) 
        filter.rating = 0
        filter.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
def color_filter_delete(request):
    if request.user.is_authenticated:     
        filter=Filter.objects.get(user=request.user)   
        filter.color = None
        filter.save()
    else:
        device=request.COOKIES["device"]
        filter=Filter.objects.get(device=device) 
        filter.color = None
        filter.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
def price_filter_delete(request):
    if request.user.is_authenticated:
        filter=Filter.objects.get(user=request.user)
        filter.price_1 = None
        filter.price_2 = None
        filter.save()
    else:
        device=request.COOKIES["device"]
        filter=Filter.objects.get(device=device) 
        filter.price_1 = None
        filter.price_2 = None
        filter.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
def size_filter_delete(request):
    if request.user.is_authenticated:
        filter=Filter.objects.get(user=request.user)
        filter.size = None
        filter.save()
    else:
        device=request.COOKIES["device"]
        filter=Filter.objects.get(device=device) 
        filter.size = None
        filter.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
def ship_filter_delete(request):
    if request.user.is_authenticated:
        filter=Filter.objects.get(user=request.user)    
        filter.shipping = False
        filter.save()
    else:
        device=request.COOKIES["device"]
        filter=Filter.objects.get(device=device)    
        filter.shipping = False
        filter.save()    
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
def manu_filter_delete(request):
    if request.user.is_authenticated:
        filter=Filter.objects.get(user=request.user)    
        filter.manufacturer = None
        filter.save()
    else:
        device=request.COOKIES["device"]
        filter=Filter.objects.get(device=device)   
        filter.manufacturer = None
        filter.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
def category_filter_delete(request):
    if request.user.is_authenticated:
        filter=Filter.objects.get(user=request.user)    
        filter.category = None
        filter.color=None
        filter.price_1 ,filter.price_2 = None,None
        filter.size=None
        filter.shipping=False
        filter.rating=None
        filter.manufacturer=None
        filter.save()
    else:
        device=request.COOKIES["device"]
        filter=Filter.objects.get(device=device)    
        filter.category = None
        filter.color=None
        filter.price_1 ,filter.price_2 = None,None
        filter.size=None
        filter.shipping=False
        filter.rating=None
        filter.manufacturer=None
        filter.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
def category(request,slug):
    category=get_object_or_404(Category,name=slug)
    manufacturer=Manufacturer.objects.filter(category=category)
    selected=0 # this is for sortings products 
    paginate=0  #this is for paginat page number 
    free=request.POST.get("free")
    size=request.POST.get("size")
    price_1=request.POST.get("price_1")
    price_2=request.POST.get("price_2")
    rate=request.POST.get("rate")
    color=request.POST.get("color")
    manu=request.POST.get("manu")  
    paginat=request.POST.get("paginat")
    select_filter=request.POST.get("select_filter")
    # product=Product.objects.order_by("-id")   
    if request.user.is_authenticated:
        repeat_user=Filter.objects.filter(user=request.user)   
        if len(repeat_user) != 1:
            for i in repeat_user[1:]:
                i.delete()    

        product_cart=Cart.objects.filter(user=request.user,ordered=True,delivered=False)
       
        filter_user,creatde=Filter.objects.get_or_create(user=request.user)
        # cart,created=Cart.pbjects
        # print(carts)   
        try:      
            device=request.COOKIES["device"]
            filter_user.device=device
            filter_user.save()
           
            if len(Filter.objects.filter(device=device)) != 1:
                for i in Filter.objects.filter(device=device):
                    i.delete()
            for i in Filter.objects.filter(user=None,device=device):
                i.user=request.user
                i.save()
            for i in product_cart:
                if i.device != device:
                    i.device =device   
                    i.save()           
                    print("product_cart saved")
            for i in Product_Cart.objects.filter(user=None,device=device,delivered=False,ordered=True):
                i.user=request.user
                i.save()
            for i in Cart.objects.filter(user=None,device=device,delivered=False,ordered=True):
                i.user=request.user
                i.save()  
            for i in Cart.objects.filter(user=request.user,ordered=True,delivered=False):
                if i.device != device:
                    i.device=device       
                    i.save()
        except:
            pass
              
              
        if free:
            try:
                filter_user.shipping=True
                filter_user.save()
            except:
                messages.error(request,"sorry,invalid value")
                pass
        if size:
            try:
                filter_user.size_id=size
                filter_user.save()    
            except:
                messages.error(request,"sorry,invalid value")
                pass

        if price_1 and price_2:
            try:
                filter_user.price_1=price_1
                filter_user.price_2=price_2
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
            
        if rate:          
            try:
                filter_user.rating=rate
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
        if color:                        
            try:
                filter_user.color_id=color 
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
        if manu:              
            try:
                filter_user.manufacturer_id=manu      
                filter_user.save()
                # print(int(manu))

            except:   
                messages.error(request,"sorry.invalid value")
                pass
        if select_filter:
            try:
                filter_user.sort= select_filter
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
        
        if paginat:
            try:
                filter_user.show= paginat
                filter_user.save() 
            except:
                messages.error(request,"sorry.invalid value")
                pass
        if filter_user.color == None and filter_user.size == None and  filter_user.manufacturer == None and filter_user.rating == None and filter_user.price_1 == None and filter_user.shipping ==False :
            if filter_user.sort == 0 or filter_user.sort == 1 or filter_user.sort == "1":
                product=Product.objects.filter(category=category).order_by("-id")   
                selected=1      
            if filter_user.sort == 2 or filter_user.sort == "2": 
                product=Product.objects.filter(category=category).order_by("id")
                selected=2  
            
            if filter_user.sort == 5 or filter_user.sort == "5":
                product=Product.objects.filter(category=category).order_by("price")
                selected=5  
                
            if filter_user.sort == 6 or filter_user.sort == "6":
                product=Product.objects.filter(category=category).order_by("-price") 
                selected=6       
        else:
            filters={}
            price_range=(filter_user.price_1,filter_user.price_2)   
            stars_range=(filter_user.rating,float(filter_user.rating) + float(0.5))
            lists={"stars__range":stars_range,"color__name":filter_user.color,"size__name":filter_user.size,"manufacturer__name":filter_user.manufacturer,"category":category,"price__range":price_range,"free_shipping":filter_user.shipping}
            # print("Ph")
   
            for i in lists:
                b=lists[i]
                if  b != None and b != (None,None) and b != (0.0,0.5):     
                    
                    filters[i]=b
               
            if filter_user.sort == 0 or filter_user.sort == 1 or filter_user.sort == "1":
                product=Product.objects.filter(**filters).order_by("-id")   
                selected=1      
            elif filter_user.sort == 2 or filter_user.sort == "2": 
        
                product=Product.objects.filter(**filters).order_by("id")
                selected=2 
            elif filter_user.sort == 5 or filter_user.sort == "5":
                product=Product.objects.filter(**filters).order_by("price")
                selected=5  
            elif filter_user.sort == 6 or filter_user.sort == "6":
                product=Product.objects.filter(**filters).order_by("-price") 
                selected=6
        # s=Cart.objects.get(user=request.user,ordered=True,delivered=False)

    else:  
        try:   
            device=request.COOKIES["device"] 
        except:     
            device=[]       
            pass        
        repeat_anonymous=Filter.objects.filter(device=device)
        if  len(repeat_anonymous) != 1:    
            for i in repeat_anonymous:   
                i.delete()
    
        # same=Product_Cart.objects.filter(device=device,ordered=True,delivered=False) 
        filter_user,created=Filter.objects.get_or_create(device=device)

        if free:
            try:
                filter_user.shipping=True
                filter_user.save()
            except:
                messages.error(request,"sorry,invalid value")
                pass
        if size:
            try:
                filter_user.size_id=size
                filter_user.save()    
            except:
                messages.error(request,"sorry,invalid value")
                pass

        if price_1 and price_2:
            try:
                filter_user.price_1=price_1
                filter_user.price_2=price_2
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
            
        if rate:          
            try:
                filter_user.rating=rate
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
        if color:                        
            try:
                filter_user.color_id=color 
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass     
        if manu:    
            try:
                filter_user.manufacturer_id=manu      
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
        if select_filter:
            try:
                filter_user.sort= select_filter  
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
        
        if paginat:
            try:
                filter_user.show= paginat
                filter_user.save() 
            except:
                messages.error(request,"sorry.invalid value")
                pass
        if  filter_user.color == None and filter_user.size == None and  filter_user.manufacturer == None and filter_user.rating == None and filter_user.price_1 == None and filter_user.shipping ==False :
            if filter_user.sort == 0 or filter_user.sort == 1 or filter_user.sort == "1" :
              
                selected=1
                product=Product.objects.filter(category=category).order_by("-id")  
            if filter_user.sort == 2 or filter_user.sort == "2":
                
                selected=2      
                product=Product.objects.filter(category=category).order_by("id")   
            if filter_user.sort == 5 or filter_user.sort == "5":
                 
                selected=5
                product=Product.objects.filter(category=category).order_by("price")  
            if filter_user.sort == 6 or filter_user.sort == "6":
            
                selected=6
                product=Product.objects.filter(category=category).order_by("-price")    
        else:      
            filters={}
            price_range=(filter_user.price_1,filter_user.price_2)
            stars_range=(filter_user.rating,float(filter_user.rating) + float(0.5))
            lists={"stars__range":stars_range,"color__name":filter_user.color,"size__name":filter_user.size,"manufacturer__name":filter_user.manufacturer,"category":category,"price__range":price_range,"free_shipping":filter_user.shipping}
            for i in lists:
                b=lists[i]
                if  b != None and b != (None,None) and b != (0.0,0.5):     
                    print(i,b)
                    filters[i]=b 
            if filter_user.sort == 0 or filter_user.sort == 1 or filter_user.sort == "1":
                product=Product.objects.filter(**filters).order_by("-id")   
                selected=1         
            elif filter_user.sort == 2 or filter_user.sort == "2": 
        
                product=Product.objects.filter(**filters).order_by("id")
                selected=2   
            elif filter_user.sort == 5 or filter_user.sort == "5":
                product=Product.objects.filter(**filters).order_by("price")
                selected=5  
            elif filter_user.sort == 6 or filter_user.sort == "6":
                product=Product.objects.filter(**filters).order_by("-price") 
                selected=6
    try:
        paginator = Paginator(product, filter_user.show) # Show requested products per page.    
        paginated=int(filter_user.show)
    except:
        paginator = Paginator(product,8 ) # Show 8 products per page.  
        paginated=8
    page_number = request.GET.get('page')    
    page_obj = paginator.get_page(page_number)                        
    context={"my_filter":filter_user,"products":page_obj,"category":category,"paginated":paginated,"selected":selected,"mani":manufacturer,"show":paginate}
    return render(request,"category.html",context)
        
def branch(request,slug):
    branch=get_object_or_404(Branch,child=slug)
    category=get_object_or_404(Category,name=branch.name)

    manufacturer=Manufacturer.objects.filter(category=branch.name)      
    selected=0 # this is for sortings products 
    paginate=0  #this is for paginat page number 
    free=request.POST.get("free")
    size=request.POST.get("size")
    price_1=request.POST.get("price_1")
    price_2=request.POST.get("price_2")
    rate=request.POST.get("rate")
    color=request.POST.get("color")
    manu=request.POST.get("manu")  
    paginat=request.POST.get("paginat")
    select_filter=request.POST.get("select_filter")
    # product=Product.objects.order_by("-id")   
    if request.user.is_authenticated:
        repeat_user=Filter.objects.filter(user=request.user)   
        if len(repeat_user) != 1:
            for i in repeat_user[1:]:
                i.delete()    

        product_cart=Cart.objects.filter(user=request.user,ordered=True,delivered=False)
       
        filter_user,creatde=Filter.objects.get_or_create(user=request.user)
        # cart,created=Cart.pbjects
        # print(carts)   
        try:      
            device=request.COOKIES["device"]
            filter_user.device=device
            filter_user.save()
           
            if len(Filter.objects.filter(device=device)) != 1:
                for i in Filter.objects.filter(device=device):
                    i.delete()
            for i in Filter.objects.filter(user=None,device=device):
                i.user=request.user
                i.save()
            for i in product_cart:
                if i.device != device:
                    i.device =device   
                    i.save()           
                    print("product_cart saved")
            for i in Product_Cart.objects.filter(user=None,device=device,delivered=False,ordered=True):
                i.user=request.user
                i.save()
            for i in Cart.objects.filter(user=None,device=device,delivered=False,ordered=True):
                i.user=request.user
                i.save()  
            for i in Cart.objects.filter(user=request.user,ordered=True,delivered=False):
                if i.device != device:
                    i.device=device       
                    i.save()
        except:
            pass
              
              
        if free:
            try:
                filter_user.shipping=True
                filter_user.save()
            except:
                messages.error(request,"sorry,invalid value")
                pass
        if size:
            try:
                filter_user.size_id=size
                filter_user.save()    
            except:
                messages.error(request,"sorry,invalid value")
                pass

        if price_1 and price_2:
            try:
                filter_user.price_1=price_1
                filter_user.price_2=price_2
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
            
        if rate:          
            try:
                filter_user.rating=rate
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
        if color:                        
            try:
                filter_user.color_id=color 
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
        if manu:              
            try:
                filter_user.manufacturer_id=manu      
                filter_user.save()
                # print(int(manu))

            except:   
                messages.error(request,"sorry.invalid value")
                pass
        if select_filter:
            try:
                filter_user.sort= select_filter
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
        
        if paginat:
            try:
                filter_user.show= paginat
                filter_user.save() 
            except:
                messages.error(request,"sorry.invalid value")
                pass
        if filter_user.color == None and filter_user.size == None and  filter_user.manufacturer == None and filter_user.rating == None and filter_user.price_1 == None and filter_user.shipping ==False :
            if filter_user.sort == 0 or filter_user.sort == 1 or filter_user.sort == "1":
                product=Product.objects.filter(branch=branch).order_by("-id")   
                selected=1      
            if filter_user.sort == 2 or filter_user.sort == "2": 
                product=Product.objects.filter(branch=branch).order_by("id")
                selected=2  
            
            if filter_user.sort == 5 or filter_user.sort == "5":
                product=Product.objects.filter(branch=branch).order_by("price")
                selected=5  
                
            if filter_user.sort == 6 or filter_user.sort == "6":
                product=Product.objects.filter(branch=branch).order_by("-price") 
                selected=6       
        else:
            filters={}
            price_range=(filter_user.price_1,filter_user.price_2)   
            stars_range=(filter_user.rating,float(filter_user.rating) + float(0.5))
            lists={"stars__range":stars_range,"color__name":filter_user.color,"size__name":filter_user.size,"manufacturer__name":filter_user.manufacturer,"branch":branch,"price__range":price_range,"free_shipping":filter_user.shipping}
            # print("Ph")
   
            for i in lists:
                b=lists[i]
                if  b != None and b != (None,None) and b != (0.0,0.5):     
                    
                    filters[i]=b
               
            if filter_user.sort == 0 or filter_user.sort == 1 or filter_user.sort == "1":
                product=Product.objects.filter(**filters).order_by("-id")   
                selected=1      
            elif filter_user.sort == 2 or filter_user.sort == "2": 
        
                product=Product.objects.filter(**filters).order_by("id")
                selected=2 
            elif filter_user.sort == 5 or filter_user.sort == "5":
                product=Product.objects.filter(**filters).order_by("price")
                selected=5  
            elif filter_user.sort == 6 or filter_user.sort == "6":
                product=Product.objects.filter(**filters).order_by("-price") 
                selected=6
        # s=Cart.objects.get(user=request.user,ordered=True,delivered=False)

    else:  
        try:   
            device=request.COOKIES["device"] 
        except:     
            device=[]       
            pass        
        repeat_anonymous=Filter.objects.filter(device=device)
        if  len(repeat_anonymous) != 1:    
            for i in repeat_anonymous:   
                i.delete()
    
        # same=Product_Cart.objects.filter(device=device,ordered=True,delivered=False) 
        filter_user,created=Filter.objects.get_or_create(device=device)

        if free:
            try:
                filter_user.shipping=True
                filter_user.save()
            except:
                messages.error(request,"sorry,invalid value")
                pass
        if size:
            try:
                filter_user.size_id=size
                filter_user.save()    
            except:
                messages.error(request,"sorry,invalid value")
                pass

        if price_1 and price_2:
            try:
                filter_user.price_1=price_1
                filter_user.price_2=price_2
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
            
        if rate:          
            try:
                filter_user.rating=rate
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
        if color:                        
            try:
                filter_user.color_id=color 
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass     
        if manu:    
            try:
                filter_user.manufacturer_id=manu      
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
        if select_filter:
            try:
                filter_user.sort= select_filter  
                filter_user.save()
            except:
                messages.error(request,"sorry.invalid value")
                pass
        
        if paginat:
            try:
                filter_user.show= paginat
                filter_user.save() 
            except:
                messages.error(request,"sorry.invalid value")
                pass
        if  filter_user.color == None and filter_user.size == None and  filter_user.manufacturer == None and filter_user.rating == None and filter_user.price_1 == None and filter_user.shipping ==False :
            if filter_user.sort == 0 or filter_user.sort == 1 or filter_user.sort == "1" :
              
                selected=1
                product=Product.objects.filter(branch=branch).order_by("-id")  
            if filter_user.sort == 2 or filter_user.sort == "2":
                
                selected=2      
                product=Product.objects.filter(branch=branch).order_by("id")   
            if filter_user.sort == 5 or filter_user.sort == "5":
                 
                selected=5
                product=Product.objects.filter(branch=branch).order_by("price")  
            if filter_user.sort == 6 or filter_user.sort == "6":
            
                selected=6
                product=Product.objects.filter(branch=branch).order_by("-price")    
        else:      
            filters={}
            price_range=(filter_user.price_1,filter_user.price_2)
            stars_range=(filter_user.rating,float(filter_user.rating) + float(0.5))
            lists={"stars__range":stars_range,"color__name":filter_user.color,"size__name":filter_user.size,"manufacturer__name":filter_user.manufacturer,"branch":branch,"price__range":price_range,"free_shipping":filter_user.shipping}
            for i in lists:
                b=lists[i]
                if  b != None and b != (None,None) and b != (0.0,0.5):     
                    print(i,b)
                    filters[i]=b 
            if filter_user.sort == 0 or filter_user.sort == 1 or filter_user.sort == "1":
                product=Product.objects.filter(**filters).order_by("-id")   
                selected=1         
            elif filter_user.sort == 2 or filter_user.sort == "2": 
        
                product=Product.objects.filter(**filters).order_by("id")
                selected=2   
            elif filter_user.sort == 5 or filter_user.sort == "5":
                product=Product.objects.filter(**filters).order_by("price")
                selected=5  
            elif filter_user.sort == 6 or filter_user.sort == "6":
                product=Product.objects.filter(**filters).order_by("-price") 
                selected=6
    try:
        paginator = Paginator(product, filter_user.show) # Show requested products per page.    
        paginated=int(filter_user.show)
    except:
        paginator = Paginator(product,8 ) # Show 8 products per page.  
        paginated=8
    page_number = request.GET.get('page')    
    page_obj = paginator.get_page(page_number)                        
    context={"my_filter":filter_user,"products":page_obj,"branch":branch,"category":category,"paginated":paginated,"selected":selected,"mani":manufacturer,"show":paginate}
    return render(request,"branch.html",context)
                       
def wishlist(request):
    if request.user.is_authenticated:
        wishlist=Wishlist.objects.filter(user=request.user)
        if len(wishlist) != 1:
           for i in wishlist:
               i.delete()    
        try:
            device=request.COOKIES["device"]
            repeat_wish=Wishlist.objects.filter(device=device)
            if len(repeat_wish) != 1:    
                for i in repeat_wish:    
                    i.delete()
            if Wishlist.objects.filter(user=request.user).exists():
                wishlist=Wishlist.objects.get(user=request.user)
                wishlist.device=device
                wishlist.save()
            if Wishlist.objects.filter(device=device,user=None).exists():
                wishlist=Wishlist.objects.get(device=device,user=None)
                wishlist.user=request.user
                wishlist.save()
            wishlist,created=Wishlist.objects.get_or_create(user=request.user,device=device)
            if len(wishlist.products.all()) == 0:
                return redirect(reverse("home:empty")) 
        except:
            wishlist,created=Wishlist.objects.get_or_create(user=request.user)
            if len(wishlist.products.all()) == 0:
                return redirect(reverse("home:empty"))
            pass

    else:     
        try:
            device=request.COOKIES["device"]
            wishlist=Wishlist.objects.filter(device=device)
            if len(wishlist) != 1:
                for i in wishlist: 
                    i.delete() 
            wishlist,created=Wishlist.objects.get_or_create(device=device)
            if len(wishlist.products.all()) == 0:
                return redirect(reverse("home:empty"))
        except:
            return redirect(reverse("home:empty"))
            pass    
    context={'wishlist':wishlist}
              
    context={'wishlist':wishlist}   
    return render(request,"wishlist.html",context)
def wishlist_add(request,id):
    product=get_object_or_404(Product,id=id)
    device=request.COOKIES["device"]
    if request.user.is_authenticated:
        repeat_list=Wishlist.objects.filter(user=request.user)
        if len(repeat_list) != 1:
            for i in repeat_list:   
                i.delete()
        list,created=Wishlist.objects.get_or_create(user=request.user)
        if product in list.products.all():
            messages.error(request,"Item already in your list") 
        else:
            list.products.add(product)
            list.device=device
            list.save()
            messages.success(request,"Item Added Successfully") 
    else:
        repeat_list=Wishlist.objects.filter(device=device)
        if len(repeat_list) != 1:
            for i in repeat_list:
                i.delete()
        list,created=Wishlist.objects.get_or_create(device=device)
        if product in list.products.all():
            messages.error(request,"Item already in your list") 
        else:
            list.products.add(product)
            messages.success(request,"Item Added Successfully") 
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def wishlist_remove(request,id):
    product=get_object_or_404(Product,id=id)
    if request.user.is_authenticated:
        repeat_list=Wishlist.objects.filter(user=request.user)
        if len(repeat_list) != 1:
            for i in repeat_list:
                i.delete()
        list=Wishlist.objects.get(user=request.user)
        if product in list.products.all():
            list.products.remove(product)
            messages.success(request,"Item Rmoved Successfully") 
        else:
            messages.error(request,"you dont have this Item in your list") 
    else:
        device=request.COOKIES["device"]
        repeat_list=Wishlist.objects.filter(device=device)
        if len(repeat_list) != 1:
            for i in repeat_list:
                i.delete()
        list=Wishlist.objects.get(device=device)
        if product in list.products.all():
            list.products.remove(product)
            messages.success(request,"Item Rmoved Successfully") 
        else:
            messages.error(request,"you dont have this Item in your list") 
  
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def wishlist_list_remove(request):
    if request.user.is_authenticated:
        repeat_list=Wishlist.objects.filter(user=request.user)
        if len(repeat_list) != 1:
            for i in repeat_list:
                i.delete()
        list=Wishlist.objects.get(user=request.user)
        list.products.remove()
        messages.success(request,"Item Rmoved Successfully") 
    else:
        device=request.COOKIES["device"]
        repeat_list=Wishlist.objects.filter(device=device)
        if len(repeat_list) != 1:
            for i in repeat_list:
                i.delete()
        list=Wishlist.objects.get(device=device)
        list.products.remove()
        messages.success(request,"Item Rmoved Successfully") 
    return redirect(reverse("home:empty"))

def test(request):
    user=User.objects.all()
    context={"user":user}    
    return render(request,"home.html",context)
  
def faq(request):
    questions=FAQ.objects.all()
    context={"questions":questions}
    return render(request,"faq.html",context)
            
def about(request):
    return render(request,"about.html")

def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        subject=request.POST.get("subject")
        message=request.POST.get("message")
        Contact.objects.create(name=name,email=email,subject=subject,message=message)
    return render(request,"contact.html")

def news(request):
    if request.user.is_authenticated:
        email=request.POST.get("email")
        if User.objects.filter(email=email).exists():
            messages.error(request,"you are already subscribed")
        else:
            NewsLetter.objects.create(user__email=email)
    else:   
        return redirect(reverse("account_login")) 
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def my_custom_page_not_found_view(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 404
    return response
  
    return response

def my_custom_error_view(request, template_name="404.html"):
    response = render(request,template_name)
    response.status_code = 500
    return response
     
    return response
def my_custom_permission_denied_view(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 403
    return response

    return response

def my_custom_bad_request_view(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 400
    return response

def dashboard(request):   
    products=Product.objects.all()
    context={"products":products}
    return render(request,"dashboard/home.html",context)
        
def add_products(request):
    form=ProductForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        print("valid")      
        instance=form.save()
        print(instance.id)
        for i in request.FILES.getlist("image"):
            Images.objects.create(product_num=instance.id,image=i)
            # form.save()  
        product= Product.objects.get(id=instance.id)
        for b in Images.objects.filter(product_num=instance.id):
            my_image=b  
            product.image.add(my_image)
    if request.is_ajax():
              
        category=request.POST.get("category")
        print(category)
        try:
            branches=Branch.objects.filter(name=category)
            response_content=list(branches.values()) 
            print(response_content)
        except Exception:   
            response_content=list({})

            response_content=list({})
        return JsonResponse(response_content,safe=False)

    context={"form":form}
    return render(request,"dashboard/products_add.html",context)

def modify_product(request,id):
    product=get_object_or_404(Product,id=id)
    form=ProductForm(request.POST or None ,request.FILES or None,instance=product)
    if form.is_valid():
        form.save()
    context={"form":form,'product':product}
    return render(request,"dashboard/product_modify.html",context)

def delete_product(request,id):
    product=get_object_or_404(Product,id=id)
    product.delete()
    return redirect(reverse("home:dashboard"))

def deals(request):
    deals=Deals.objects.all()
    context={"deals":deals}
    return render(request,"dashboard/deals.html",context)
def deals_add(request):
    if len(Deals.objects.filter(expired=False)) >= 2:
        messages.error(request,"maximum 2 Deals ")
        return redirect(reverse("home:deals"))
    form =DealForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse("home:deals"))
    context={"form":form}
    return render(request,"dashboard/deals_add.html",context)

def deals_delete(request,id):
    deals=Deals.objects.get(id=id)
    deals.delete()
    return redirect(reverse("home:deals"))

def category_dash(request):
    category=Category.objects.all()
    return render(request,"dashboard/category.html",{"category":category})
    
def category_add(request):
    form =CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse("home:category"))
    context={"form":form}
    return render(request,"dashboard/category_add.html",context)

def category_delete(request,id):
    category=Category.objects.get(id=id)
    category.delete()
    return redirect(reverse("home:category"))

def branch(request):
    branch=Branch.objects.all()
    return render(request,"dashboard/branch.html",{"branch":branch})
    
def branch_add(request):
    form =BranchForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse("home:branch"))
    context={"form":form}
    return render(request,"dashboard/branch_add.html",context)

def branch_delete(request,id):
    branch=Branch.objects.get(id=id)
    branch.delete()       
    return redirect(reverse("home:branch"))

def manu(request):
    manu=Manufacturer.objects.all()
    return render(request,"dashboard/manu.html",{"manu":manu})
    
def manu_add(request):
    form =ManuForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse("home:manu"))
    context={"form":form}
    return render(request,"dashboard/manu_add.html",context)

def manu_delete(request,id):
    manu=Manufacturer.objects.get(id=id)
    manu.delete()       
    return redirect(reverse("home:manu"))


def search(request):
    qs = request.GET.get("q")
    product=Product.objects.filter(Q(name__icontains=qs)| Q(category__name__icontains=qs)|Q(branch__child__icontains=qs)|Q(details__icontains=qs)).distinct()
    paginator = Paginator(product,2)
    page_num =  request.GET.get("page")
    page_obj = paginator.get_page(page_num)       
    return render(request,"search.html")
