from .models import *                                                                                                                                                 
from django.core.paginator import Paginator
from django.shortcuts import render,redirect,reverse
from django.contrib import messages

def global_newsletter(request):
    news=NewsLetter.objects.first()
    value=False                                                                           
    if request.user.is_authenticated:
        user=request.user
        # for i in news.all():
        # if len(news.user) != 0:
            #     news=False
        if user in news.user.all():
            print("here")
            value=True
        # else:
        #     news.user.add(user)
        #     value=True
    else:
        value=False
        # for i in news.user.all()
    context={"value":value}
    return context
def global_profile(request):
    if request.user.is_authenticated:
        profile=Profile.objects.get(user=request.user)
    else:
        profile=[]
        # messageserror(request,"please login First....")
        # return redirect(reverse("account_login"))
    context={"profile":profile}
    return  context
def global_wishlist(request):     
    if request.user.is_authenticated:    

        wishlist=Wishlist.objects.filter(user=request.user)
        if len(wishlist) != 1:
           for i in wishlist[1:]:
               i.delete()      
               
        try:
            device=request.COOKIES["device"]
            repeat_wish=Wishlist.objects.filter(device=device)
            if len(repeat_wish) != 1:    
                for i in repeat_wish[1:]:    
                    i.delete()
                  
            if Wishlist.objects.filter(user=request.user).exists():
                wishlist=Wishlist.objects.get(user=request.user)
                wishlist.device=device
                wishlist.save()
            if Wishlist.objects.filter(device=device,user=None).exists():
                wishlist=Wishlist.objects.get(device=device,user=None)
                wishlist.user=request.user
                wishlist.save()
            lists=Wishlist.objects.filter(user=request.user,device=device)
            if len(lists) != 1:
                for i in lists[1:]:
                    i.delete()
            wishlist,created=Wishlist.objects.get_or_create(user=request.user,device=device)
           
        except:
            wishlist,created=Wishlist.objects.get_or_create(user=request.user)

            pass

    else:      
        try:
            device=request.COOKIES["device"]
            wishlist=Wishlist.objects.filter(device=device)
            if len(wishlist) != 1:
                for i in wishlist[1:]:
                    i.delete() 
                  
            wishlist,created=Wishlist.objects.get_or_create(device=device)
           
        except:
            wishlist={}
          
            pass    
    context={'wishlist':wishlist}
    return context
def global_context(request):        
    if request.user.is_authenticated:

        repeat_cart=Cart.objects.filter(user=request.user,ordered=True,delivered=False)
        # order=
        if len(repeat_cart) != 1:    
            for i in repeat_cart[1:]:
                i.delete()
        try:
            device=request.COOKIES['device']
            repeat_cart=Cart.objects.filter(device=device,ordered=True,delivered=False)
            if len(repeat_cart) != 1:
                for i in repeat_cart[1:]:
                    i.delete()
            if Cart.objects.filter(user=request.user,ordered=True,delivered=False).exists():
                cart=Cart.objects.get(user=request.user,ordered=True,delivered=False)
                cart.device=device
                cart.save()
                for i in cart.products.all():
                    i.device=device
                    i.save()
                print("saved device")
            if Cart.objects.filter(device=device,user=None,ordered=True,delivered=False).exists():
                cart=Cart.objects.get(device=device,user=None,ordered=True,delivered=False)
                cart.user=request.user
                cart.save()
                for i in cart.products.all():
                    i.user=request.user
                    i.save()
            for i in Product_Cart.objects.filter(user=request.user,ordered=True,delivered=False):
                i.device=device
                i.save()
            repeat_device_product=Product_Cart.objects.filter(device=device,user=None,ordered=True,delivered=False)
            for i in repeat_device_product:
                i.user=request.user
                i.save()
            for i in Product_Cart.objects.filter(user=request.user,ordered=True,delivered=False):
                i.device=device
                i.save()
            carts=Cart.objects.filter(user=request.user,device=device,ordered=True,delivered=False)
            if len(carts) != 1:
                for i in carts[1:]:
                    i.delete()
            cart,created=Cart.objects.get_or_create(user=request.user,device=device,ordered=True,delivered=False)
        except:
            cart,created=Cart.objects.get_or_create(user=request.user,ordered=True,delivered=False)
            pass    
    else:    
        for i in Cart.objects.all():
            print(i.user,i.device,i.id)
        try:        
            device=request.COOKIES["device"]     
            repeat_cart=Cart.objects.filter(device=device,ordered=True,delivered=False)
            if len(repeat_cart) !=1:
                for i in repeat_cart[1:]:
                    i.delete()
            cart,created=Cart.objects.get_or_create(device=device,ordered=True,delivered=False)
        except:    
            cart=[]     
            pass
    context={"cart":cart}
    return context           

     