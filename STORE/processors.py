from .models import *                                                                                                                                                 
from django.core.paginator import Paginator
from django.shortcuts import render,redirect,reverse
from django.contrib import messages
from accept.payment import *
import requests
  
  
API_KEY="ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6VXhNaUo5LmV5SmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljSEp2Wm1sc1pWOXdheUk2TVRFNE1ESTVMQ0p1WVcxbElqb2lhVzVwZEdsaGJDSjkuU0VhV0IwbjlMVklMeHVKd1NqTFVldDNWc0pqMDVMZjBOVUNuTmZROGZJOFdxREswb3FUOE1pYjBUeTY2MHlXZzRsUGNXU3dhTHZDc0x5RVd1LUtRaVE=" #PAYMOB

def global_PayMob(request):
    if request.user.is_authenticated:
        try:
            order=Order.objects.get(user=request.user,ordered=True,delivered=False)
            # if order.track_number:
            
            accept = AcceptAPI(API_KEY)
            trans=accept.inquire_transaction(merchant_order_id=order.id,order_id=order.track_number)
            if trans["success"] == True:
                order.track_number=trans["id"]
                order.delivered=True
                order.cart.delivered=True  
                print("here")
                for i in order.cart.products.all():
                    i.delivered=True
                    i.products.most_buy +=1
                    i.products.save()
                    i.save()
                order.cart.save()
                order.save()
                print(trans)
      
        except: 
            order=0
            print("not trans") 
            
            pass      
    else:
        order=0
        pass
    context={"trans":order} 
    return context
    
    
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
            try:
                if len(wishlist) > 1:
                    wishlist=Wishlist.objects.filter(device=device).latest("modified_date")
                else:
                    wishlist=Wishlist.objects.get(device=device)
            except:
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
            # if len(repeat_cart) != 1:
            #     for i in repeat_cart[1:]:
            #         i.delete()
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
        try:        
            device=request.COOKIES["device"]     
            repeat_cart=Cart.objects.filter(device=device,ordered=True,delivered=False)
            # if len(repeat_cart) !=1:
            #     for i in repeat_cart[1:]:
            #         i.delete()
            try:
                if len(repeat_cart) > 1:
                    cart=Cart.objects.filter(device=device,ordered=True,delivered=False).latest("modified_date")

                else:    
                    cart=Cart.objects.get(device=device,ordered=True,delivered=False)
                print("here")
            except:
                cart=Cart.objects.create(device=device,ordered=True,delivered=False)
                print("created")
        except:      
            cart=[]     
            pass
    context={"cart":cart}
    return context           

    
def global_ajax(request):
    if request.is_ajax():
        ajax="ajax"
        print(ajax)
    else:
        ajax="not here"
        print(ajax)
    context={"ajax":ajax}
    return context