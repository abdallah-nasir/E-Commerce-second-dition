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
# Create your views here.    


     
def home(request):
    return render(request,"home.html")
def products(request):
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
        product_cart=Product_Cart.objects.filter(user=request.user,ordered=True,delivered=False)
        filter_user,creatde=Filter.objects.get_or_create(user=request.user)
        # cart,created=Cart.pbjects
        # print(carts)   
        try:   
            device=request.COOKIES["device"]
            filter_user.device=device
            filter_user.save()
            print("saved")   
            for i in repeat_user:
                if i.device != device:
                    i.delete()      
                    print("delete") 
            for i in Product_Cart.objects.filter(user=None,device=device,delivered=False,ordered=True):
                i.user=request.user
                i.save()
            for i in Cart.objects.filter(user=None,device=device,delivered=False,ordered=True):
                i.user=request.user
                i.save()  
            for i in Cart.objects.filter(user=request.user,ordered=True,delivered=False):
                i.device=device       
                i.save()
            for i in product_cart:
                if i.device != device:    
                    i.device =device
                    i.save()           
                    print("product_cart saved")

        except:
            pass
            print("passed")
              
        if free:
            filter_user.shipping=True
            filter_user.save()
            print("free")
        if size:
            filter_user.size_id=size
            filter_user.save()    
            print("size")     

        if price_1 and price_2:
            filter_user.price_1=price_1
            filter_user.price_2=price_2
            filter_user.save()
            print("price_1")
        if rate:       
            filter_user.rating_id=rate
            filter_user.save()
            print("rate")
        if color:                      
            filter_user.color_id=color 
            filter_user.save()
            print("color")
        if manu:    
            filter_user.manufacturer_id=manu      
            filter_user.save()
            print("manu")  
        if select_filter:
            filter_user.sort= select_filter
            filter_user.save()
        if paginat:
            filter_user.show= paginat
            filter_user.save() 
        if filter_user.category == None and filter_user.color == None and filter_user.size == None and  filter_user.manufacturer == None and filter_user.rating == None and filter_user.price_1 == None and filter_user.shipping ==False :
            if filter_user.sort == "1":
                product=Product.objects.order_by("-id")   
                selected=1      
            elif filter_user.sort == "2": 
                print("asdasd")
                product=Product.objects.order_by("id")
                selected=2 
            elif filter_user.sort == "5":
                product=Product.objects.order_by("price")
                selected=5  
            elif filter_user.sort == "6":
                product=Product.objects.order_by("-price") 
                selected=6
            else:
                product=Product.objects.order_by("-id") 

            print("none")
        else:
            filters={}
            price_range=(filter_user.price_1,filter_user.price_2)
            product=Product.objects.filter(price__range=(filter_user.price_1,filter_user.price_2))  
            lists={"price__range":price_range,"size__name":filter_user.size,"color_id":filter_user.color,"category__name":filter_user.category,"free_shipping":filter_user.shipping,"manufacturer__name":filter_user.manufacturer}
            for i in lists:
                b=lists[i]
                if  b != None and b != (None,None):     
                    print(i,b)
                    filters[i]=b
            product=Product.objects.filter(**filters)

    else:  
        try:   
            device=request.COOKIES["device"] 
            print("anonymous device")
        except:     
            device=[]
            pass     
        print("passed anonymous")
        repeat_anonymous=Filter.objects.filter(device=device)
        product_cart=Product_Cart.objects.filter(device=device,ordered=True)     
        filter_user,creatde=Filter.objects.get_or_create(device=device)
        filter_user.device=device
        filter_user.save()
        for i in repeat_anonymous:
            if i.device != device:
                i.delete()      
                print("delete")      
        for i in product_cart:
            if i.device != device:
                i.device =device
                i.save()           
                print("product_cart saved") 
        if free:
            filter_user.shipping=True
            filter_user.save()
            print("free")
        if size:
            filter_user.size_id=size  
            filter_user.save()
            print("size")     
        if price_1 and price_2:
            filter_user.price_1=price_1
            filter_user.price_2=price_2
            filter_user.save()
            print("price_1")
        if rate:       
            filter_user.rating_id=rate
            filter_user.save()
            print("rate")
        if color:                      
            filter_user.color_id=color 
            filter_user.save()
            print("color")
        if select_filter:
            filter_user.sort= select_filter
            filter_user.save()
        if paginat:
            filter_user.show= paginat
            filter_user.save() 
        if filter_user.category == None and filter_user.color == None and filter_user.size == None and  filter_user.manufacturer == None and filter_user.rating == None and filter_user.price_1 == None and filter_user.shipping ==False :
            if select_filter == 2 :
                print(select_filter)
                selected=2
                product=Product.objects.order_by("id")         # else:
            else:
                product=Product.objects.order_by("-id")         # else:

            print("none")     
        #     product=Product.objects.filter(price__range=(filter_user.price_1,filter_user.price_2),color_id=filter_user.color,free_shipping=filter_user.shipping,category_id=filter_user.category)  
        else:      
            filters={}
            price_range=(filter_user.price_1,filter_user.price_2)
            product=Product.objects.filter(price__range=(filter_user.price_1,filter_user.price_2))  
            lists={"price__range":price_range,"size__name":filter_user.size,"color_id":filter_user.color,"category__name":filter_user.category,"free_shipping":filter_user.shipping,"manufacturer__name":filter_user.manufacturer}
            for i in lists:
                b=lists[i]
                if  b != None and b != (None,None):     
                    print(i,b)
                    filters[i]=b
            product=Product.objects.filter(**filters)
    paginator = Paginator(product, 2) # Show 25 contacts per page.    
                  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)                     
    context={"carts":product_cart,"my_filter":filter_user,"products":page_obj,"selected":selected,"show":paginate}
    return render(request,"products.html",context)
    
def color_filter_delete(request):
    if request.user.is_authenticated:
        filter=Filter.objects.get(user=request.user)
        filter.color = None
        filter.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def price_filter_delete(request):
    if request.user.is_authenticated:
        filter=Filter.objects.get(user=request.user)
        filter.price_1 = None
        filter.price_2 = None
        filter.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
def size_filter_delete(request):
    if request.user.is_authenticated:
        filter=Filter.objects.get(user=request.user)
        filter.size = None
        filter.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
def ship_filter_delete(request):
    if request.user.is_authenticated:
        filter=Filter.objects.get(user=request.user)    
        filter.shipping = False
        filter.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def manu_filter_delete(request):
    if request.user.is_authenticated:
        filter=Filter.objects.get(user=request.user)    
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
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def category(request,slug):
    category=get_object_or_404(Category,name=slug)
    selected=0 # this is for sortings products 
    paginate=0  #this is for paginat page number 
    free=request.POST.get("free")
    size=request.POST.get("size")
    price_1=request.POST.get("price_1")     
    price_2=request.POST.get("price_2")
    rate=request.POST.get("rate")
    color=request.POST.get("color") 
    manu=request.POST.get("manu")  
    # product=Product.objects.order_by("-id")
    if request.user.is_authenticated:
        repeat_user=Filter.objects.filter(user=request.user)   
        product_cart=Product_Cart.objects.filter(user=request.user,ordered=True,delivered=False)
        filter_user,creatde=Filter.objects.get_or_create(user=request.user)
        # cart,created=Cart.pbjects
        # print(carts)   
        try:   
            device=request.COOKIES["device"]
            filter_user.device=device
            filter_user.save()
            print("saved")   
            for i in repeat_user:
                if i.device != device:
                    i.delete()      
                    print("delete") 
            for i in Product_Cart.objects.filter(user=None,device=device,delivered=False,ordered=True):
                i.user=request.user
                i.save()
            for i in Cart.objects.filter(user=None,device=device,delivered=False,ordered=True):
                i.user=request.user
                i.save()  
            for i in Cart.objects.filter(user=request.user,ordered=True,delivered=False):
                i.device=device       
                i.save()
            for i in product_cart:
                if i.device != device:    
                    i.device =device
                    i.save()           
                    print("product_cart saved")

        except:
            pass
            print("passed")
              
        if free:
            filter_user.shipping=True
            filter_user.save()
            print("free")
        if size:
            filter_user.size_id=size
            filter_user.save()    
            print("size")     

        if price_1 and price_2:
            filter_user.price_1=price_1
            filter_user.price_2=price_2
            filter_user.save()
            print("price_1")
        if rate:       
            filter_user.rating_id=rate
            filter_user.save()
            print("rate")
        if color:                      
            filter_user.color_id=color 
            filter_user.save()
            print("color")
        if manu:    
            filter_user.manufacturer_id=manu      
            filter_user.save()
            print("manu")    
        if filter_user.category == None and filter_user.color == None and filter_user.size == None and  filter_user.manufacturer == None and filter_user.rating == None and filter_user.price_1 == None and filter_user.shipping ==False :
            product=Product.objects.filter(category=category).order_by("-id")         # else:
            print("none")
        #     product=Product.objects.filter(price__range=(filter_user.price_1,filter_user.price_2),color_id=filter_user.color,free_shipping=filter_user.shipping,category_id=filter_user.category)  
        else:
            filters={}
            price_range=(filter_user.price_1,filter_user.price_2)
            product=Product.objects.filter(price__range=(filter_user.price_1,filter_user.price_2))  
            lists={"price__range":price_range,"size__name":filter_user.size,"color_id":filter_user.color,"category":category,"free_shipping":filter_user.shipping,"manufacturer__name":filter_user.manufacturer}
            for i in lists:
                b=lists[i]
                if  b != None and b != (None,None):     
                    print(i,b)
                    filters[i]=b
            product=Product.objects.filter(**filters)
              
    else:  
        try:   
            device=request.COOKIES["device"] 
            print("anonymous device")
        except:     
            device=[]
            pass     
        print("passed anonymous")
        repeat_anonymous=Filter.objects.filter(device=device)
        product_cart=Product_Cart.objects.filter(device=device,ordered=True)     
        filter_user,creatde=Filter.objects.get_or_create(device=device)
        filter_user.device=device
        filter_user.save()
        for i in repeat_anonymous:
            if i.device != device:
                i.delete()      
                print("delete")      
        for i in product_cart:
            if i.device != device:
                i.device =device
                i.save()           
                print("product_cart saved") 
        if free:
            filter_user.shipping=True
            filter_user.save()
            print("free")
        if size:
            filter_user.size_id=size  
            filter_user.save()
            print("size")     
        if price_1 and price_2:
            filter_user.price_1=price_1
            filter_user.price_2=price_2
            filter_user.save()
            print("price_1")
        if rate:       
            filter_user.rating_id=rate
            filter_user.save()
            print("rate")
        if color:                      
            filter_user.color_id=color 
            filter_user.save()
            print("color")
          
        if filter_user.category == None and filter_user.color == None and filter_user.size == None and  filter_user.manufacturer == None and filter_user.rating == None and filter_user.price_1 == None and filter_user.shipping ==False :
            product=Product.objects.filter(category=category).order_by("-id")         # else:
            print("none")     
        #     product=Product.objects.filter(price__range=(filter_user.price_1,filter_user.price_2),color_id=filter_user.color,free_shipping=filter_user.shipping,category_id=filter_user.category)  
        else:      
            filters={}
            price_range=(filter_user.price_1,filter_user.price_2)
            product=Product.objects.filter(price__range=(filter_user.price_1,filter_user.price_2))  
            lists={"price__range":price_range,"size__name":filter_user.size,"color_id":filter_user.color,"category":category,"free_shipping":filter_user.shipping,"manufacturer__name":filter_user.manufacturer}
            for i in lists:
                b=lists[i]
                if  b != None and b != (None,None):     
                    print(i,b)
                    filters[i]=b
            product=Product.objects.filter(**filters)
    paginator = Paginator(product, 2) # Show 25 contacts per page.    
        
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)           
    context={"my_filter":filter_user,"products":page_obj,"selected":selected,"show":paginate,"category":category}
    return render(request,"category.html",context)
    
def add_to_cart(request,id):
    device=request.COOKIES["device"]
    product=get_object_or_404(Product,id=id)
    if request.user.is_authenticated:
        repeat_product=Product_Cart.objects.filter(user=request.user,delivered=False)
        for i in repeat_product:
            if i.device != device:
                i.device=device
                print("reapeat product")
        repeat_cart=Cart.objects.filter(user=request.user,ordered=True,delivered=False)
        for i in repeat_cart:
            if i.device != device:
                i.ddevice=device
                print("repeat cart")
        product_cart,created=Product_Cart.objects.get_or_create(products=product,user=request.user,delivered=False)
        product_cart.device=device
        product_cart.save()
        print("prodcut_cart authenticated")
        for i in Cart.objects.filter(user=request.user,ordered=True,delivered=False):
            if i.device != device:
                i.delete()    
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
       
def wishlist(request):
    if request.user.is_authenticated:
        wishlist=Wishlist.objects.filter(user=request.user)
    else:
        try:
            device=request.COOKIES["device"]
        except: 
            device=[]
            pass
        wishlist=Wishlist.objects.filter(device=device)
    context={}
    return render(request,"wishlist.html",context)
def wishlist_add(request,id):
    product=get_object_or_404(Product,id=id)
    device=request.COOKIES["device"]
    if request.user.is_authenticated:
        list,created=Wishlist.objects.get_or_create(user=request.user)
        if product in list.products.all():
            messages.error(request,"Item already in your list") 
        else:
            list.products.add(product)
            list.device=device
            list.save()
            messages.success(request,"Item Added Successfully") 
    else:
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
        list=Wishlist.objects.get(user=request.user)
        if product in list.products.all():
            list.products.remove(product)
            messages.success(request,"Item Rmoved Successfully") 
        else:
            messages.error(request,"you dont have this Item in your list") 
    else:
        list=Wishlist.objects.get(device=device)
        if product in list.products.all():
            list.products.remove(product)
            messages.success(request,"Item Rmoved Successfully") 
        else:
            messages.error(request,"you dont have this Item in your list") 
  
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

     
     

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
            Images.objects.create(product_num=instance.id,image=form.cleaned_data.get("image"))
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