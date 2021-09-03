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
from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string

from django.conf import settings
from cities_light.models import Country,Region
from django.contrib.auth.decorators import login_required
from accept.payment import * 
# Create your views here.    
from datetime import date   
import time
from django.utils import timezone
from django.utils.timezone import get_current_timezone
from itertools import chain
def search(request):
    selected=0 # this is for sortings products   
    paginate=0  #this is for paginat page number
    free=request.POST.get("shipping")
    price_1=request.POST.get("price_1")
    price_2=request.POST.get("price_2")
    rate=request.POST.get("rate")
    paginat=request.POST.get("paginat")
    select_filter=request.POST.get("select_filter")
    category=Category.objects.all()
    if request.method == "POST": 
        if free:
            request.session["shipping"] = True
        if price_1:
            request.session["price_1"] = price_1
        if price_2:
            request.session["price_2"] = price_2
        if rate:
            request.session["rate"] = rate
        if paginat:
            request.session["paginat"] = paginat
        if select_filter:
            request.session["select_filter"] = select_filter
    try:
        if request.session["shipping"] == True:
            shipping=True
        else:
            shipping=None
    except:
        shipping=None
    try:
        if request.session["price_1"] != None:
            price_1=request.session.get("price_1")
        else:
            price_1=None
    except:
        price_1=None
    try:
        if request.session["price_2"] != None:
            price_2=request.session.get("price_2")
        else:
            price_2=None
    except:
        price_2=None
    try:
        if request.session["rate"] != None:
            rating=request.session.get("rate")
            for i in range(int(rating)):
                loop =i
                loop +=1        
        else:
            rating=None
            loop =False
    except:
        rating=None
        loop =False
    try:
        if request.session["paginat"] != None:
            paginat=request.session["paginat"]
        else:
            paginat=None
    except:
        paginat=None
    try:
        if request.session["select_filter"] != None:
            select_filter=request.session["select_filter"]
            print(select_filter)
        else:
            select_filter=None
    except:
        select_filter=None
    try:           
        qs=request.GET["qs"]
        search=f"qs={qs}"  
        q1=Product.objects.filter(Q(name__icontains=qs) |Q(details__icontains=qs) | Q(category__name__icontains=qs) | Q(branch__child__icontains=qs) | Q(manufacturer__name__icontains=qs) | Q(color__name__icontains=qs)).distinct()
        filters={}
        price_range=(price_1,price_2)   
        # print(price_range)
        try:
            count=float(rating) + float(0.5)
            stars_range=(int(rating),float(count))
           
        except:
            stars_range=(0,0.5)
           
        lists={"stars__range":stars_range,"price__range":price_range,"free_shipping":shipping}
        for i in lists:
            b=lists[i]
            if  b != None and b != (None,None) and b != (0.0,0.5):     
                filters[i]=b
        if select_filter == 0 or select_filter == 1 or select_filter == "1" or select_filter == None:
            product=q1.filter(**filters).distinct().order_by('-id')
            selected=1         
        elif select_filter == 2 or select_filter == "2": 
            product=q1.filter(**filters).distinct().order_by('id')
            selected=2   
        elif select_filter == 5 or select_filter == "5":
            product=q1.filter(**filters).distinct().order_by('price')
            selected=5     
        elif select_filter == 6 or select_filter == "6":
            product=q1.filter(**filters).distinct().order_by('-price')
            selected=6
       
    except:  
        search=None
        product=Product.objects.none()
        filter_user={}      
        paginated={}  
    try:
        paginator = Paginator(product, int(paginat)) # Show requested products per page.    
        paginated=int(paginat)
    except:
        paginator = Paginator(product,8 ) # Show 8 products per page.  
        paginated=8
   
    page_number = request.GET.get('page')      
    page_obj = paginator.get_page(page_number)     
    context={"category":category,"paginated":paginated,"selected":selected,"shipping":shipping,"loop":loop,"price_1":price_1,"price_2":price_2,"rate":rating,"search":search,"products":page_obj}
    return render(request,"search.html",context)

def shipping_session(request):
    request.session["shipping"] = None
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
def manu_session(request):
    request.session["manu"] = None
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
def size_session(request):
    request.session["size"] = None
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def price_session(request):
    request.session["price_1"],request.session["price_2"] = None,None
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def rating_session(request):
    request.session["rate"] = None
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

def home(request):
    trend=Product.objects.order_by("-stars")[0:12]
    arrivals=Product.objects.order_by("-id")[0:8]
    category=Category.objects.all()   
    most_buy=Product.objects.order_by("-most_buy")[0:4]
    for i in Deals.objects.filter(expired=False):
        if i.expire_date.date() < date.today() or i.expire_date.date() == date.today():
            i.expired=True
            i.save()   
    deal=Deals.objects.filter(expired=False) 

    context={"deals":deal,"paid":most_buy,"trend":trend,"arrivals":arrivals,"category":category}
    return render(request,"home.html",context)   
def products(request):
    category=Category.objects.all()
    selected=0 # this is for sortings products   
    paginate=0  #this is for paginat page number
    free=request.POST.get("shipping")
    price_1=request.POST.get("price_1")
    price_2=request.POST.get("price_2")
    rate=request.POST.get("rate")
    paginat=request.POST.get("paginat")
    select_filter=request.POST.get("select_filter")
    manu=request.POST.get("manu")
    size=request.POST.get("size")
    

    if request.method == "POST": 
        if free:
            request.session["shipping"] = True
        if price_1:
            request.session["price_1"] = price_1
        if price_2:
            request.session["price_2"] = price_2
        if rate:
            request.session["rate"] = rate
        if paginat:
            request.session["paginat"] = paginat
        if select_filter:
            request.session["select_filter"] = select_filter
        if manu:
            request.session["manu"] = manu
        if size:
            request.session["size"] = size
    try:
        if request.session["shipping"] == True:
            shipping=True
        else:
            shipping=None
    except:
        shipping=None
    try:
        if request.session["price_1"] != None:
            price_1=request.session.get("price_1")
        else:
            price_1=None
    except:
        price_1=None
    try:
        if request.session["price_2"] != None:
            price_2=request.session.get("price_2")
        else:
            price_2=None
    except:
        price_2=None
    try:
        if request.session["rate"] != None:
            rating=request.session.get("rate")
            for i in range(int(rating)):
                loop =i
                loop +=1        
               
        else:
            rating=None
            loop =False
    except:
        rating=None
        loop =False
    try:
        if request.session["paginat"] != None:
            paginat=request.session["paginat"]
        else:
            paginat=None
    except:
        paginat=None
    try:
        if request.session["select_filter"] != None:
            select_filter=request.session["select_filter"]
           
        else:
            select_filter=None
    except:
        select_filter=None

    if shipping == None and price_2 == None and rating == None and manu == None :
    
        if select_filter == 0 or select_filter == 1 or select_filter == "1" or select_filter == None:
            product=Product.objects.all().order_by("-id")   
            selected=1      
        if select_filter == 2 or select_filter == "2": 
            product=Product.objects.all().order_by("id")
            selected=2  
         
        if select_filter == 5 or select_filter == "5":
            product=Product.objects.all().order_by("price")
            selected=5  
               
        if select_filter == 6 or select_filter == "6":
            product=Product.objects.all().order_by("-price") 
            selected=6  
   
            
    else:  
        print("filterd")
        filters={}
        price_range=(price_1,price_2)   
        try:
            count=float(rating) + float(0.5)
            stars_range=(int(rating),float(count))    
        except:  
            stars_range=(0,0.5)
    
        lists={"stars__range":stars_range,"price__range":price_range,"free_shipping":shipping}

        for i in lists:
            b=lists[i]
            if  b != None and b != (None,None) and b != (0.0,0.5):     
                filters[i]=b
        if select_filter == 0 or select_filter == 1 or select_filter == "1" or select_filter == None:
            product=Product.objects.filter(**filters).distinct().order_by('-id')
            selected=1         
        elif select_filter == 2 or select_filter == "2": 
            product=Product.objects.filter(**filters).distinct().order_by('id')
            selected=2   
        elif select_filter == 5 or select_filter == "5":
            product=Product.objects.filter(**filters).distinct().order_by('price')
            selected=5     
        elif select_filter == 6 or select_filter == "6":
            product=Product.objects.filter(**filters).distinct().order_by('-price')
            selected=6
        
      
    try:
        paginator = Paginator(product, int(paginat)) # Show requested products per page.    
        paginated=int(paginat)
      
    except:  
        paginator = Paginator(product,8 ) # Show 8 products per page.  
        paginated=8

    page_number = request.GET.get('page')      
    page_obj = paginator.get_page(page_number)                       
    context={"products":page_obj,"category":category,"paginated":paginated,
             "selected":selected,
             "shipping":shipping,"price_1":price_1,"price_2":price_2,
             "size":size,"rating":rating,"loop":loop,"show":paginate}
    return render(request,"products.html",context)
   
def this_product(request,id):

    product=get_object_or_404(Product,id=id)
    same=Product.objects.filter(category=product.category).order_by("-id")[0:4]
    reviews=Rate.objects.filter(product__id=product.id) #specific rate for particular product
    form=RateForm(request.POST or None)
    comments=request.POST.get("comments")
    if comments:
        print(comments)
        if comments == "1":    
            details=Rate_Details.objects.filter(rate_id__in=reviews,product=product).order_by("-stars","-id")   #details for this rate
            details_order=1
        if comments == "2":
            details=Rate_Details.objects.filter(rate_id__in=reviews,product=product).order_by("stars","-id")   #details for this rate
            details_order=2
    else:
        details=Rate_Details.objects.filter(rate_id__in=reviews,product=product).order_by("-stars","-id")   #details for this rate
        details_order=1
    if form.is_valid():            
      if request.is_ajax():   
        print("ajax")
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
                # print(my_rate.count)  
                date= f"{my_rate.date.strftime('%b')}, {my_rate.date.day}, {my_rate.date.year}, {my_rate.date.hour}:{my_rate.date.minute}"
                # print(date)
                data={"comment_user":my_rate.rate.user.username.title(),"comment_date":date, 
                      "comment_stars":my_rate.stars,"comment_average":my_rate.product.average()["average"],
                      'comment':my_rate.review,"comment_count":my_rate.ajax_len()}   
                print(data)   
                return JsonResponse(data)    
            except:
                new_rate=Rate.objects.create(user=request.user)   
                new_rate.product.add(product)
                new_rate.save()    
                my_rate=Rate_Details.objects.create(rate_id=new_rate.id,product=product,review=review,stars=stars)
                product.stars +=float(stars)    
                product.save()
                print("created") 
                date= f"{my_rate.date.strftime('%b')}, {my_rate.date.day}, {my_rate.date.year}, {my_rate.date.hour}:{my_rate.date.minute}"
                data={"comment_user":my_rate.rate.user.username.title(),"comment_date":date, 
                      "comment_stars":my_rate.stars,"comment_average":my_rate.product.average()["average"],
                      'comment':my_rate.review,"comment_count":my_rate.ajax_len()}      
                print(data)
                return JsonResponse(data)
        else:
            messages.error(request,"you should login first")
            return redirect(reverse("account_login"))    

    context={"details_order":details_order,"product":product,"same":same,"form":form,"reviews":reviews,"details":details}
    return render(request,"this_product.html",context)

def cart(request):
    countries=Country.objects.all()
    if request.is_ajax():
        country=request.POST.get("country")
        region=request.POST.get('region')

        try:
            my_region=Region.objects.filter(country_id=country)           
            cities=City.objects.filter(region_id=region)
            response_content=cities.values()
            if country:
                response_content=my_region.values()
            elif region:
                response_content=cities.values()
        except Exception:       
            response_content=list({})        
        return JsonResponse(list(response_content),safe=False)        
        
    if request.user.is_authenticated:  
        try:     
            device=request.COOKIES["device"]
            cart=Cart.objects.filter(user=request.user,ordered=True,delivered=False).latest("modified_date")
            cart.device = device
            cart.save()
            if len(cart.products.all()) == 0:
                return redirect(reverse("home:empty"))
        except:
            return redirect(reverse("home:empty"))
    else:   
        try:    
            device=request.COOKIES["device"]
            cart=Cart.objects.filter(device=device,ordered=True,delivered=False).latest("modified_date")
            if len(cart.products.all()) == 0:
                return redirect(reverse("home:empty"))
        except:
            return redirect(reverse("home:empty"))
    context={"countries":countries} 
    return render(request,"cart.html",context)
  
def shipping_cost(request,id):  
    cart=Cart.objects.get(id=id)
    price=cart.price
    country=request.POST.get("country")
    try:
        shipping=Shipping.objects.get(id=country)
    except: 
        pass
    cart.shipping=shipping
    cart.save()
    return redirect(reverse("home:cart"))
  
def empty(request):
      
    return render(request,"empty.html")   

  
@login_required()
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
   
@login_required() 
def make_new_address(request):
    profile=Profile.objects.get(user=request.user)
    phone=request.POST.get("phone")
    street=request.POST.get("street")
    city=request.POST.get("city")
    country=request.POST.get("country")
    region=request.POST.get("region")
    zip=request.POST.get("zip")                      
    if len(Address.objects.filter(profile=profile)) >= 3:   
        messages.error(request,"sorry,you should have 3 Address only")
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:     
        try:
            Address.objects.create(profile=profile,phone=phone,street=street,country_id=country,region_id=region,city_id=city,zip=zip)
        except:  
            messages.error(request,"sorry, invalid data")
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required()
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
                return redirect(reverse("home:order",kwargs={"id":order.cart.id}))
            else:
                return (redirect(reverse("home:order_confirm",kwargs={"id":order.id})))
        else:
            print(payment)
            messages.error(request,"sorry, invalid payment option")
            return redirect(reverse("home:order",kwargs={"id":order.cart.cart.id}))
    except:
        messages.error(request,"sorry,invalid payment option")
        return redirect(reverse("home:order",kwargs={"id":order.id}))
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


### payment views

from paypalcheckoutsdk.orders import OrdersCreateRequest
from paypalcheckoutsdk.orders import OrdersCaptureRequest
from paypalcheckoutsdk.core import SandboxEnvironment,PayPalHttpClient
CLIENT_ID="AXRoqNBK6jhVc6UqCteZ69SvMvng9d0dglftwbI1VDUlmCpgwJ5EZPGUxmon1-ZaUzTiKHEWiIwxDTO8" #paypal
CLIENT_SECRET="EISXMlwWduSB8zNUb0MuUUEtcmsnW4IZ865QnFdwwyskNZcajh3GPFqSLZd-mfcgXxuhO0ul-NF8sxOr" #paypl
API_KEY="ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKSVV6VXhNaUo5LmV5SmpiR0Z6Y3lJNklrMWxjbU5vWVc1MElpd2ljSEp2Wm1sc1pWOXdheUk2TVRFNE1ESTVMQ0p1WVcxbElqb2lhVzVwZEdsaGJDSjkuU0VhV0IwbjlMVklMeHVKd1NqTFVldDNWc0pqMDVMZjBOVUNuTmZROGZJOFdxREswb3FUOE1pYjBUeTY2MHlXZzRsUGNXU3dhTHZDc0x5RVd1LUtRaVE=" #PAYMOB

@login_required()
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
        print(data)
        return JsonResponse(data)
    else:
        return JsonResponse({'details': "invalide request"})
        print("not herer")

def capture(request,order_id,id):       
    if request.method=="POST": 
        capture_order = OrdersCaptureRequest(order_id)
        environment = SandboxEnvironment(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
        client = PayPalHttpClient(environment)
        response = client.execute(capture_order)
        data = response.result.__dict__['_dict']
        try:
            order=Order.objects.get(user=request.user,ordered=True,delivered=False,id=id)
            
            for i in order.cart.products.all():
                i.delivered=True 
                i.products.most_buy +=1
                i.save()
                i.products.save()
            order.cart.delivered=True
            order.cart.save()
            order.delivered=True
            order.track_number=data["id"]
            order.save()
            msg_html = render_to_string("email_order_confirm.html",{"order":order})
            msg = EmailMessage(subject="order confirm", body=msg_html, from_email=settings.EMAIL_HOST_USER, to=[order.user.email])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
        except:
            pass
    return redirect(reverse("home:success"))
@login_required()
def order_confirm(request,id):
    try:
        order=Order.objects.get(id=id,user=request.user,ordered=True,delivered=False)
        if order.payments == "Cash on Delivery":
            order_payment=1
        elif order.payments == "PayPal":
            order_payment=2
        elif order.payments == "Credit / Debit Card":
            order_payment=3
        elif order.converter() == None:
            return redirect(reverse('home:cart'))

        else:
            return redirect(reverse('home:cart'))
        payment=None 
    except:
        return redirect(reverse('home:home'))
    if order.payments == 'Cash on Delivery':
        order.track_number=order.id
        order.delivered=True
        order.cart.delivered=True  
        for i in order.cart.products.all():
            i.delivered=True
            i.products.most_buy +=1
            i.products.save()
            i.save()
        order.cart.save()
        order.save()
        msg_html = render_to_string("email_order_confirm.html",{"order":order})
        msg = EmailMessage(subject="order confirm", body=msg_html, from_email=settings.EMAIL_HOST_USER, to=[order.user.email])
        msg.content_subtype = "html"  # Main content is now text/html
        msg.send()   
        return redirect(reverse("home:success"))
    try:
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
            msg_html = render_to_string("email_order_confirm.html",{"order":order})
            msg = EmailMessage(subject="order confirm", body=msg_html, from_email=settings.EMAIL_HOST_USER, to=[order.user.email])
            msg.content_subtype = "html"  # Main content is now text/html
            msg.send()
            return redirect(reverse("home:success"))
    except:    
        pass
    payment_token=None
    if order.payments == "Credit / Debit Card":
        convert=order.converter()
        url_1="https://accept.paymob.com/api/auth/tokens"
        data_1={"api_key": API_KEY}
        r_1=requests.post(url_1,json=data_1)
        token=r_1.json().get("token")
        print(token)
        data_2={
  "auth_token": token,
  "delivery_needed": "false",
  "amount_cents": order.egy_currency*100,
  "currency": "EGP",
  "merchant_order_id": order.id + 62,
  "items": [
    {
        "name": "ASC1515",
        "amount_cents": "500000",
        "description": "Smart Watch",
        "quantity": "1"
    },
    {  
        "name": "ERT6565",
        "amount_cents": "200000",
        "description": "Power Bank",
        "quantity": "1"
    }
    ],
  "shipping_data": {
    "apartment": "803", 
    "email": "claudette09@exa.com", 
    "floor": "42", 
    "first_name": "Clifford", 
    "street": "Ethan Land", 
    "building": "8028", 
    "phone_number": "+86(8)9135210487", 
    "postal_code": "01898", 
     "extra_description": "8 Ram , 128 Giga",
    "city": "Jaskolskiburgh", 
    "country": "CR", 
    "last_name": "Nicolas", 
    "state": "Utah"
  },
    "shipping_details": {
        "notes" : " test",
        "number_of_packages": 1,
        "weight" : 1,
        "weight_unit" : "Kilogram",
        "length" : 1,
        "width" :1,
        "height" :1,
        "contents" : "product of some sorts"
    }
}
        url_2="https://accept.paymob.com/api/ecommerce/orders"
        r_2=requests.post(url_2,json=data_2)
        my_id=r_2.json().get("id")
        try:
            order.track_number=my_id
            order.save()
     

        except:
            pass

        if my_id == None:
            print("none")
            r_2=requests.get(url_2,json=data_2)
            my_id=r_2.json().get("results")[0]["id"]  
        print(my_id)
        if order.delivered ==True:
            return redirect(reverse("home:home"))    
        data_3={   
  "auth_token":token, 
  "amount_cents": order.egy_currency*100, 
  "expiration": 3600, 
  "order_id": my_id,   
  "billing_data": {
    "apartment": "803", 
    "email": "claudette09@exa.com", 
    "floor": "42", 
    "first_name": "Clifford", 
    "street": "Ethan Land", 
    "building": "8028", 
    "phone_number": "+86(8)9135210487", 
    "shipping_method": "PKG", 
    "postal_code": "01898",   
    "city": "Jaskolskiburgh", 
    "country": "CR", 
    "last_name": "Nicolas", 
    "state": "Utah"
  }, 
  "currency": "EGP", 
  "integration_id": 585334,
  "lock_order_when_paid": "false"
}
        url_3="https://accept.paymob.com/api/acceptance/payment_keys"
        r_3=requests.post(url_3,json=data_3)
        payment_token=(r_3.json().get("token"))
        print(payment_token)  
    context={"order_payment":order_payment,"order":order,"frame": 270151,"payment":payment_token}
    return render(request,"order_confirm.html",context)


    
########
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

@login_required()
def order(request,id):
    countries=Country.objects.all()

    profile=get_object_or_404(Profile,user=request.user)
    repeat_order=Order.objects.filter(user=request.user,ordered=True,delivered=False)
    if len(repeat_order) != 1:
        for i in repeat_order:
            i.delete()
    repeat_cart=Cart.objects.filter(user=request.user,ordered=True,delivered=False)
    if len(repeat_cart) != 1:
        for i in repeat_cart[1:]:     
            i.delete()
    cart=get_object_or_404(Cart,user=request.user,ordered=True,delivered=False,id=id) 
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
        zip=request.POST.get("zip")
        default=request.POST.get("default")
        primary=request.POST.get("primary")
        country=request.POST.get("country")
        region=request.POST.get('region')
        if request.is_ajax():
            try:  
                my_region=Region.objects.filter(country_id=country)           
                cities=City.objects.filter(region_id=region)
                response_content=cities.values()
                if country:
                    response_content=my_region.values()
                elif region:
                    response_content=cities.values()
            except Exception:       
                response_content=list({})        
            return JsonResponse(list(response_content),safe=False)
        if len(Address.objects.filter(profile=profile)) >= 3:
            messages.error(request,"sorry,you should have 3 Address only")
            return redirect(reverse("home:order",kwargs={"id":cart.id}))       

        if default == None:
            try:
                address=Address.objects.create(profile=profile,phone=phone,street=street,country_id=country,region_id=region,city_id=city,zip=zip)              
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
                return redirect(reverse("home:order",kwargs={"id":order.cart.id}))  
            except:
                messages.error(request,"invalid data")   
                return redirect(reverse("home:order",kwargs={"id":order.cart.id}))
        elif default == "on":
            
            try: 
                address=Address.objects.get(profile=profile,primary=True)
                order.address=address
                order.save()
                if notes:     
                    order.notes=notes
                    order.save()  
                    print("on")
            except:
                messages.error(request,"you dont have a primary address")
                return redirect(reverse("home:order",kwargs={"id":cart.id}))

    context={"order":order,"countries":countries,"my_address":my_address,"all":all_address}
    return render(request,"checkout.html",context)

@login_required()
def profile(request,slug):    
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


    context={"profile":profile,"all":all_order,"order":order,"canceled":canceled_order,"info":info}
    return render(request,"profile.html",context)

@login_required()
def profile_account(request,slug):   
    profile=Profile.objects.get(user=request.user)
    order=Order.objects.filter(ordered=True,delivered=True,user=request.user).exclude(statue="canceled").count()
    canceled_order=Order.objects.filter(ordered=True,delivered=True,user=request.user,statue="canceled").count()


    context={"profile":profile,"order":order,"canceled":canceled_order}
    return render(request,"profile_account.html",context)
@login_required()
def profile_edit(request,slug):   
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


    context={"profile":profile,"order":order,"canceled":canceled_order,"form":form}
    return render(request,"profile_edit.html",context)

@login_required()
def address(request,slug):

    countries=Country.objects.all()
    profile=Profile.objects.get(user=request.user)
    info=Address.objects.filter(profile=profile)
    order=Order.objects.filter(ordered=True,delivered=True,user=request.user).exclude(statue="canceled").count()
    canceled_order=Order.objects.filter(ordered=True,delivered=True,user=request.user,statue="canceled").count()
    if request.is_ajax():
        region=request.POST.get("region")
        country=request.POST.get("country")
        city=request.POST.get("city")
        print(country,region)
        try:
            my_region=Region.objects.filter(country_id=country)           
            cities=City.objects.filter(region_id=region)
            response_content=cities.values()
            if country:
            
                response_content=my_region.values()
            elif region:
                response_content=cities.values()
        except Exception:       
            response_content=list({})         
        return JsonResponse(list(response_content),safe=False)        
    if len(info) >= 3:
        len_info=True   
    else:
        len_info=False

    context={"profile":profile,"len_info":len_info,"countries":countries,"info":info,"canceled":canceled_order,"order":order}
    return render(request,"address_book.html",context)

@login_required()
def address_add(request,slug):    
    countries=Country.objects.all()
    profile=Profile.objects.get(user=request.user)
    info=Address.objects.filter(profile=profile)
    order=Order.objects.filter(ordered=True,delivered=True,user=request.user).exclude(statue="canceled").count()
    canceled_order=Order.objects.filter(ordered=True,delivered=True,user=request.user,statue="canceled").count()
    if len(info) >= 3:
            return redirect(reverse("home:address",kwargs={"slug":profile.user}))
    else:
        if request.method == 'POST':
            country=request.POST.get("country")
            city=request.POST.get("city")
            region=request.POST.get("region")
            phone=request.POST.get("phone")
            street=request.POST.get("street")
            zip=request.POST.get("zip")
            if request.is_ajax():
                
                try:
                    my_region=Region.objects.filter(country_id=country)           
                    cities=City.objects.filter(region_id=region)
                    response_content=cities.values()
                    if country:
                        response_content=my_region.values()
                    elif region:
                        response_content=cities.values()
                except Exception:       
                    response_content=list({})        
                return JsonResponse(list(response_content),safe=False)        
    
            try:
                print(country,region,city)
                address=Address.objects.create(profile=profile,phone=phone,street=street,country_id=country,region_id=region,city_id=city,zip=zip)
                if len(Address.objects.filter(profile=profile)) ==1:
                    address.primary=True
                    address.save()
                messages.success(request,"Address Added successfully")
                return redirect(reverse("home:address",kwargs={"slug":profile.user}))
            except:
                messages.error(request,"invalid data")   
                return redirect(reverse("home:address_add",kwargs={"slug":profile.user}))

 

    context={"profile":profile,"countries":countries,"canceled":canceled_order,"order":order,"info":info}
    return render(request,"address_add.html",context)

@login_required()
def address_edit(request,id):
    address=Address.objects.get(profile__user=request.user,id=id)
    form=AddressEdit(request.POST or None,instance=address)
    if form.is_valid():
        form.save()
        return redirect(reverse("home:address",kwargs={"slug":request.user}))
    else:
        messages.error(request,"invalid data")
    return redirect(reverse("home:address",kwargs={"slug":request.user}))
   
@login_required()
def order_track(request,slug):    
    profile=Profile.objects.get(user=request.user)
    order=Order.objects.filter(ordered=True,delivered=True,user=request.user).exclude(statue="canceled").count()
    canceled_order=Order.objects.filter(ordered=True,delivered=True,user=request.user,statue="canceled").count()
    track=request.POST.get("track")
    if request.method == "POST":
        try:
            my_order=Order.objects.get(user=request.user,track_number=track) #user=request.user,ordered=True,delivered=True,
        except:  
            my_order=False     
    else:
        my_order={}

  
    context={"profile":profile,"order":order,"canceled":canceled_order,"my_orders":my_order}

    return render(request,"order_track.html",context)

@login_required()
def manage_order(request,slug):
    profile,created=Profile.objects.get_or_create(user=request.user)
    try:
        my_order=Order.objects.get(user=request.user,ordered=True,delivered=True) #user=request.user,ordered=True,delivered=True,
    except:
        return redirect(reverse("home:empty"))    

    context={"order":my_order}
    return render(request,'manage_order.html',context)
@login_required()
def canceled_order(request,slug):
    profile=Profile.objects.get(user=request.user)
    my_order=Order.objects.filter(user=request.user,ordered=True,delivered=True,statue="canceled") #user=request.user,ordered=True,delivered=True,
    order=Order.objects.filter(ordered=True,delivered=True,user=request.user).exclude(statue="canceled").count()
    canceled_order=Order.objects.filter(ordered=True,delivered=True,user=request.user,statue="canceled").count()

    context={"my_order":my_order,"order":order,"canceled":canceled_order}
    return render(request,'canceled_order.html',context)

def category(request,slug):
    category=get_object_or_404(Category,name=slug)
    manufacturer=Manufacturer.objects.filter(category=category)
    sizes=Size.objects.all()
    selected=0 # this is for sortings products   
    paginate=0  #this is for paginat page number
    free=request.POST.get("shipping")
    price_1=request.POST.get("price_1")
    price_2=request.POST.get("price_2")
    rate=request.POST.get("rate")
    paginat=request.POST.get("paginat")
    select_filter=request.POST.get("select_filter")
    manu=request.POST.get("manu")
    size=request.POST.get("size")
    

    if request.method == "POST": 
        if free:
            request.session["shipping"] = True
        if price_1:
            request.session["price_1"] = price_1
        if price_2:
            request.session["price_2"] = price_2
        if rate:
            request.session["rate"] = rate
        if paginat:
            request.session["paginat"] = paginat
        if select_filter:
            request.session["select_filter"] = select_filter
        if manu:
            request.session["manu"] = manu
        if size:
            request.session["size"] = size
    try:
        if request.session["shipping"] == True:
            shipping=True
        else:
            shipping=None
    except:
        shipping=None
    try:
        if request.session["price_1"] != None:
            price_1=request.session.get("price_1")
        else:
            price_1=None
    except:
        price_1=None
    try:
        if request.session["price_2"] != None:
            price_2=request.session.get("price_2")
        else:
            price_2=None
    except:
        price_2=None
    try:
        if request.session["rate"] != None:
            rating=request.session.get("rate")
            for i in range(int(rating)):
                loop =i
                loop +=1        
               
        else:
            rating=None
            loop =False
    except:
        rating=None
        loop =False
    try:
        if request.session["paginat"] != None:
            paginat=request.session["paginat"]
        else:
            paginat=None
    except:
        paginat=None
    try:
        if request.session["select_filter"] != None:
            select_filter=request.session["select_filter"]
           
        else:
            select_filter=None
    except:
        select_filter=None
    try:
        if request.session["manu"] != None:
            manu=request.session["manu"]
           
        else:
            manu=None
    except:
        manu=None
    try:
        if request.session["size"] != None:
            size=request.session["size"]
           
        else:
            size=None
    except:
        size=None
    if shipping == None and price_2 == None and rating == None and manu == None :
    
        if select_filter == 0 or select_filter == 1 or select_filter == "1" or select_filter == None:
            product=Product.objects.filter(category=category).order_by("-id")   
            selected=1      
        if select_filter == 2 or select_filter == "2": 
            product=Product.objects.filter(category=category).order_by("id")
            selected=2  
         
        if select_filter == 5 or select_filter == "5":
            product=Product.objects.filter(category=category).order_by("price")
            selected=5  
               
        if select_filter == 6 or select_filter == "6":
            product=Product.objects.filter(category=category).order_by("-price") 
            selected=6  
   
            
    else:  
        print("filterd")
        filters={}
        price_range=(price_1,price_2)   
        try:
            count=float(rating) + float(0.5)
            stars_range=(int(rating),float(count))    
        except:  
            stars_range=(0,0.5)
        print(stars_range)
        lists={"stars__range":stars_range,"manufacturer__name":manu,"size__name":size,"price__range":price_range,"category":category,"free_shipping":shipping}

        for i in lists:
            b=lists[i]
            if  b != None and b != (None,None) and b != (0.0,0.5):     
                filters[i]=b
        if select_filter == 0 or select_filter == 1 or select_filter == "1" or select_filter == None:
            product=Product.objects.filter(**filters).distinct().order_by('-id')
            selected=1         
        elif select_filter == 2 or select_filter == "2": 
            product=Product.objects.filter(**filters).distinct().order_by('id')
            selected=2   
        elif select_filter == 5 or select_filter == "5":
            product=Product.objects.filter(**filters).distinct().order_by('price')
            selected=5     
        elif select_filter == 6 or select_filter == "6":
            product=Product.objects.filter(**filters).distinct().order_by('-price')
            selected=6
        
   
    try:
        paginator = Paginator(product, int(paginat)) # Show requested products per page.    
        paginated=int(paginat)
      
    except:  
        paginator = Paginator(product,8 ) # Show 8 products per page.  
        paginated=8

    page_number = request.GET.get('page')      
    page_obj = paginator.get_page(page_number)                       
    context={"products":page_obj,"category":category,"paginated":paginated,
             "selected":selected,"mani":manufacturer,"manu":manu,
             "shipping":shipping,"price_1":price_1,"price_2":price_2,
             "size":size,"sizes":sizes,"rating":rating,"loop":loop,"show":paginate}
    return render(request,"category.html",context)
        
def branch(request,slug):
    branch=get_object_or_404(Branch,child=slug)
    category=get_object_or_404(Category,name=branch.name)
    manufacturer=Manufacturer.objects.filter(category=category)
    sizes=Size.objects.all()
    selected=0 # this is for sortings products   
    paginate=0  #this is for paginat page number
    free=request.POST.get("shipping")
    price_1=request.POST.get("price_1")
    price_2=request.POST.get("price_2")
    rate=request.POST.get("rate")
    paginat=request.POST.get("paginat")
    select_filter=request.POST.get("select_filter")
    manu=request.POST.get("manu")
    size=request.POST.get("size")
    

    if request.method == "POST": 
        if free:
            
            request.session["shipping"] = True
        if price_1:
            request.session["price_1"] = price_1
        if price_2:
            request.session["price_2"] = price_2
        if rate:
            request.session["rate"] = rate
        if paginat:
            request.session["paginat"] = paginat
        if select_filter:
            request.session["select_filter"] = select_filter
            print(select_filter)
        if manu:
            request.session["manu"] = manu
        if size:
            request.session["size"] = size
    try:
        if request.session["shipping"] == True:
            shipping=True
        else:
            shipping=None
    except:
        shipping=None
    try:
        if request.session["price_1"] != None:
            price_1=request.session.get("price_1")
        else:
            price_1=None
    except:
        price_1=None
    try:
        if request.session["price_2"] != None:
            price_2=request.session.get("price_2")
        else:
            price_2=None
    except:
        price_2=None
    try:
        if request.session["rate"] != None:
            rating=request.session.get("rate")
            for i in range(int(rating)):
                loop =i
                loop +=1        
               
        else:
            rating=None
            loop =False
    except:
        rating=None
        loop =False
    try:
        if request.session["paginat"] != None:
            paginat=request.session["paginat"]
        else:
            paginat=None
    except:
        paginat=None
    try:
        if request.session["select_filter"] != None:
            select_filter=request.session["select_filter"]
           
        else:
            select_filter=None
    except:
        select_filter=None
    try:
        if request.session["manu"] != None:
            manu=request.session["manu"]
           
        else:
            manu=None
    except:
        manu=None
    try:
        if request.session["size"] != None:
            size=request.session["size"]
           
        else:
            size=None
    except:
        size=None
    if shipping == None and price_2 == None and rating == None and manu == None :
    
        if select_filter == 0 or select_filter == 1 or select_filter == "1" or select_filter == None:
            product=Product.objects.filter(branch=branch).order_by("-id")   
            selected=1       
        if select_filter == 2 or select_filter == "2": 
            product=Product.objects.filter(branch=branch).order_by("id")
            selected=2  
         
        if select_filter == 5 or select_filter == "5":
            product=Product.objects.filter(branch=branch).order_by("price")
            selected=5  
               
        if select_filter == 6 or select_filter == "6":
            product=Product.objects.filter(branch=branch).order_by("-price") 
            selected=6      
        # else: 
        #     product=Product.objects.filter(branch=branch)
            
    else:     
        print("filterd")
        filters={}
        price_range=(price_1,price_2)   
        try:
            count=float(rating) + float(0.5)
            stars_range=(int(rating),float(count))    
        except:  
            stars_range=(0,0.5)
    
        lists={"stars__range":stars_range,"manufacturer__name":manu,"size__name":size,"price__range":price_range,"branch":branch,"free_shipping":shipping}

        for i in lists:
            b=lists[i]
            if  b != None and b != (None,None) and b != (0.0,0.5):     
                filters[i]=b
        if select_filter == 0 or select_filter == 1 or select_filter == "1":
            product=Product.objects.filter(**filters).distinct().order_by('-id')
            selected=1         
        elif select_filter == 2 or select_filter == "2": 
            product=Product.objects.filter(**filters).distinct().order_by('id')
            selected=2   
        elif select_filter == 5 or select_filter == "5":
            product=Product.objects.filter(**filters).distinct().order_by('price')
            selected=5     
        elif select_filter == 6 or select_filter == "6":
            product=Product.objects.filter(**filters).distinct().order_by('-price')
            selected=6
        
   
    try:
        paginator = Paginator(product, int(paginat)) # Show requested products per page.    
        paginated=int(paginat)
      
    except:  
        paginator = Paginator(product,8 ) # Show 8 products per page.  
        paginated=8
    print(rating)
    page_number = request.GET.get('page')      
    page_obj = paginator.get_page(page_number)                       
    context={"products":page_obj,"branch":branch,"paginated":paginated,
             "selected":selected,"mani":manufacturer,"manu":manu,
             "shipping":shipping,"price_1":price_1,"price_2":price_2,
             "size":size,"sizes":sizes,"rating":rating,"loop":loop,"show":paginate}
    return render(request,"branch.html",context)
                       
def wishlist(request):
    if request.user.is_authenticated:
        try:
            wishlist=Wishlist.objects.filter(user=request.user).latest("modified_date")
            if len(wishlist.products.all()) == 0:
                return redirect(reverse("home:empty"))
        except:
            return redirect(reverse("home:empty"))
    else:   
        try:    
            device=request.COOKIES["device"]
            wishlist=Wishlist.objects.filter(device=device)
            if len(wishlist) > 1:
                wishlist=Wishlist.objects.filter(device=device).latest("modified_date")
                if len(wishlist.products.all()) == 0:
                    return redirect(reverse("home:empty"))
            else:
                wishlist=Wishlist.objects.get(device=device)
                if len(wishlist.products.all()) == 0:
                    return redirect(reverse("home:empty"))
        except:
            return redirect(reverse("home:empty"))
                
    context={'wishlist':wishlist}   
    return render(request,"wishlist.html",context)

def wishlist_add(request):
    try:
        id=request.GET["id"]
    except:
        messages.error(request,"invalid data")
        return redirect(reverse("home:wishlist"))
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
            data={"id":list.id}
            return JsonResponse(data)
    else:     
        repeat_list=Wishlist.objects.filter(device=device)
        if len(repeat_list) > 1:
            list=Wishlist.objects.filter(device=device).latest("modified_date")
            if product in list.products.all():
                messages.error(request,"Item already in your list") 
            else:
                list.products.add(product)
                messages.success(request,"Item Added Successfully") 
                data={"id":list.id}
                return JsonResponse(data)
        else:  
            try:
                list=Wishlist.objects.filter(device=device).latest("modified_date")
            except:
                list=Wishlist.objects.create(device=device)
                print("created")
            if product in list.products.all():
                messages.error(request,"Item already in your list") 
            else:   
                print(list.id)

                list.products.add(product)
                messages.success(request,"Item Added Successfully") 
                data={"id":list.id}
                return JsonResponse(data)
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
     
def wishlist_remove(request):
    try:
        id=request.GET["id"]
    except:
        messages.error(request,"invalid data")
        return redirect(reverse("home:wishlist"))
    product=get_object_or_404(Product,id=id)
    if request.user.is_authenticated:    
        list=Wishlist.objects.filter(user=request.user).latest("modified_date")
        if product in list.products.all():
            list.products.remove(product)
            messages.success(request,"Item Rmoved Successfully") 
            data={"id":list.id}
            return JsonResponse(data)
        else:
            messages.error(request,"you dont have this Item in your list") 
    else:
        device=request.COOKIES["device"]
        repeat_list=Wishlist.objects.filter(device=device)
        if len(repeat_list) > 1:
            list=Wishlist.objects.filter(device=device).latest("modified_date")
            if product in list.products.all():
                list.products.remove(product)
                messages.success(request,"Item Rmoved Successfully") 
                data={"id":list.id}
                return JsonResponse(data)    
            else:
                messages.error(request,"you dont have this Item in your list") 
        else:                                       
            try:
                list=Wishlist.objects.filter(device=device).latest("modified_date")
                if product in list.products.all():
                    list.products.remove(product)
                    messages.success(request,"Item Rmoved Successfully") 
                    data={"id":list.id}
                    return JsonResponse(data)    
                else:
                    messages.error(request,"you dont have this Item in your list") 
            except:
                pass
            
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
  
def wishlist_list_remove(request):
    if request.user.is_authenticated:
        list=Wishlist.objects.filter(user=request.user).latest("modified_date")
        list.products.remove()
        messages.success(request,"Item Rmoved Successfully") 
    else:
        device=request.COOKIES["device"]
        repeat_list=Wishlist.objects.filter(device=device)
        if len(repeat_list) > 1:
            list=Wishlist.objects.filter(device=device).latest("modified_date")
            list.products.remove()
            messages.success(request,"Item Rmoved Successfully") 
            data={"id":list.id}
            return JsonResponse(data)    
        else:  
            try:
                list=Wishlist.objects.filter(device=device).latest("modified_date")
                list.products.remove()
                messages.success(request,"Item Rmoved Successfully") 
                data={"id":list.id}
                return JsonResponse(data)    
            except:
                pass
    return redirect(reverse("home:empty"))

def cart_clear(request):
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user,ordered=True,delivered=False).latest("modified_date")
        for i in cart.products.all():    
            i.delete()
    else:
        device=request.COOKIES["device"]
        cart=Cart.objects.filter(device=device,ordered=True,delivered=False).latest("modified_date")
        for i in cart.products.all():    
            i.delete()
    return redirect(reverse("home:cart"))

def add_to_cart(request):
    device=request.COOKIES["device"]
    try:
        id=request.GET["id"]
        print(id)
    except:
        messages.error(request,"invalid data")
        return redirect(reverse("home:products"))
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
            for i in product_cart.products.image.all():
                image_url=i.image
            image=product_cart.products.image.first().image
    
                      
    
            data={"id":product_cart.id,"amounts":cart.order_product_length(),
                "product_category":product_cart.products.category.name,"product_name":product_cart.products.name,
                "product_price":product_cart.product_price_individual(),"product_quantity":product_cart.quantity,
                "product_image":str(image),"product_url":product_cart.get_url(),
                "product_category_url":product_cart.get_category_url(),"total":cart.before_discount(),
                "product_remove":product_cart.get_cart_remove_url()} 
            print(data)   
            return JsonResponse(data)
    else:
        device=request.COOKIES["device"]   
        try:
            product_cart=Product_Cart.objects.filter(products=product,device=device,delivered=False).latest("modified_date")
        except:
            product_cart=Product_Cart.objects.create(products=product,device=device,delivered=False)

        print("prodcut_cart anonymous")
        try:
            if len(Cart.objects.filter(device=device,ordered=True,delivered=False)) > 1:
                cart=Cart.objects.filter(device=device,ordered=True,delivered=False).latest("modified_date")
            else:
                cart=Cart.objects.get(device=device,ordered=True,delivered=False) 
        except:
            cart=Cart.objects.create(device=device,ordered=True,delivered=False)

        if product_cart in cart.products.all():     
            messages.error(request,"this item is in your cart")
        else:
            cart.products.add(product_cart)  
            product_cart.ordered=True     
            product_cart.save()    
            cart.save()
            print("cart anonymous")         
            image=product_cart.products.image.first().image

            messages.success(request,"Item Added Successfully") 
            data={"id":product_cart.id,"amounts":cart.order_product_length(),
                "product_category":product_cart.products.category.name,"product_name":product_cart.products.name,
                "product_price":product_cart.product_price_individual(),"product_quantity":product_cart.quantity,
                "product_image":str(image),"product_url":product_cart.get_url(),
                "product_category_url":product_cart.get_category_url(),"total":cart.before_discount(),
                "product_remove":product_cart.get_cart_remove_url()} 
            print(data)   
            return JsonResponse(data)
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    
        # product_cart.

def cart_quantity_add(request):
    try:
        device=request.COOKIES["device"]
        id=request.GET["id"]
        product_cart=Product_Cart.objects.get(id=id)
        print(id)
    except:
        print("passed")
        messages.error(request,"invalid data")
        return redirect(reverse("home:cart"))
    if product_cart.quantity >= 10:
        messages.error(request,"you have reached the maximum quantity")
        return redirect(reverse("home:cart"))
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user,ordered=True,delivered=False).latest("modified_date")
    else:
        cart=Cart.objects.filter(device=device,ordered=True,delivered=False).latest("modified_date")
    if request.is_ajax():
        print("ajax")
        product_cart.quantity +=1
        product_cart.save()
        data={"id":product_cart.id,"total":cart.before_discount(),"price":product_cart.product_price_individual(),"quantity":product_cart.quantity}
        # response_content=product_cart
        return JsonResponse(data)   
    return redirect(reverse("home:cart"))
    
def cart_quantity_remove(request):
    try:
        device=request.COOKIES["device"]
        id=request.GET["id"]
        product_cart=Product_Cart.objects.get(id=id)
        
    except:
        print("passed")
        messages.error(request,"invalid data")
        return redirect(reverse("home:cart"))
    if request.user.is_authenticated:
        cart=Cart.objects.filter(user=request.user,ordered=True,delivered=False).latest("modified_date")
    else:
        cart=Cart.objects.filter(device=device,ordered=True,delivered=False).latest("modified_date")
    if request.is_ajax():
        product_cart.quantity -=1
        product_cart.save()
        if product_cart.quantity <= 0:
            product_cart.delete()
        data={"id":product_cart.id,"total":cart.before_discount(),"price":product_cart.product_price_individual(),"quantity":product_cart.quantity}
        return JsonResponse(data)   

    return redirect(reverse("home:cart"))
    

   
def remove_from_cart(request):
   
    try:  
        id=request.GET["id"]
        device=request.COOKIES["device"]
        product=None
        if request.user.is_authenticated:
            cart=Cart.objects.filter(user=request.user,ordered=True,delivered=False).latest("modified_date")
            print(cart)
        else:
            cart=Cart.objects.filter(device=device)
            if len(cart) > 1:
                cart=Cart.objects.filter(device=device).latest("modified_date")
            else:
                cart=Cart.objects.get(device=device)
        for i in cart.products.all():
            print(i)
            if i.id == int(id):
                product=i.id
                i.delete()
              
    
      
        messages.success(request,"Item removed Successfully")
    
        data={"id":product,"amounts":cart.order_product_length(),
              "total":cart.before_discount(),}
        print(data)   
        return JsonResponse(data)
    except:
        print("except")
        messages.error(request,"invalid data")
        
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
          
def quick_add(request,id):
    quantity=request.POST.get("quantity")
    if request.user.is_authenticated:
        try:
            device=request.COOKIES["device"]
            product,created=Product_Cart.objects.get_or_create(user=request.user,products_id=id,ordered=True,delivered=False)
            product.quantity +=int(quantity)
            product.device=device
            product.save()
            cart=Cart.objects.filter(user=request.user,ordered=True,delivered=False).latest("modified_date")
            cart.products.add(product)
            cart.device=device
            cart.save()
        except:
            messages.error(request,"invalid data")
    else:
        try:
            device=request.COOKIES["device"]
            product,created=Product_Cart.objects.get_or_create(device=device,products_id=id,ordered=True,delivered=False)
            product.quantity +=int(quantity)
            product.device=device 
            product.save()
            cart=Cart.objects.filter(device=device,ordered=True,delivered=False).latest("modified_date")
            cart.products.add(product)
            cart.device=device
            cart.save()
        except:
            messages.error(request,"invalid data")
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

import csv    
def test(request):   
    # url=requests.get("https://deals.souq.com/eg-en/computers/c/13414")
    # details_url=requests.get("https://egypt.souq.com/eg-en/lenovo-yoga-9-14itl5-laptop-intel-core-i7-1185g7-14-inch-uhd-1tb-ssd-16-gb-ram-integrated-intel-iris-xe-graphics-windows-shadow-black-14968700075/u/")
    # souq=bss4(url.text,"lxml")
    # products=souq.findAll("div",{"class":"column column-block block-grid-large"})
    # details=bss4(details_url.text,"lxml")
    # pro__details=details.findAll("div",{"class":"item-details-mini clearfix"})
    # for i in Images.objects.all():
    #     i.save()
    # print(pro__details)    
    # with open("details.csv","w",newline="") as file:
        # writer =csv.writer(file)     
        # writer.writerow(["name","price","image","url"])
        # print(details)    
        # for product in products:
        #     name=product.find("h6","title").text
        #     price=product.find("h5","price").text
        #     image=product.find("img","img-size-medium")["data-src"]
        #     url=product.find("a","img-link imgShowQuickView")["href"]
            # print(price)           
            # writer.writerow([name,price,image,url])          

    # with open('laptops.csv') as csv_file:
    #     csv_reader = csv.reader(csv_file)
    #     for row in csv_reader: 
    #         product=Product.objects.create(name=row[0],price=int(row[1]),details="any details",stock=100)
    #         images=Images.objects.create(image__url=row[2])
    #         product.image.add(images)
    #         product.save()  
   
    #         print(details_url)
     
    # category_url=requests.get("https://fakestoreapi.com/products/categories")
    # product_url=requests.get('https://fakestoreapi.com/products')
    # products=product_url.json()
    # categories=category_url.json()
    # for i in categories:
    #    category=Category.objects.create(name=i)
    #    Branch.objects.create(name=category,child=i)
    # for i in products:
    #     for c in Category.objects.all():
    #         if c.name == i["category"]:
    #             cat=c
    #     for b in Branch.objects.all():
    #         if b.child == i["category"]: 
    #             child=b
    #     product= Product.objects.create(name=i["title"],price=i["price"],branch=b,stock=100,category=cat,details=i["description"])
    #     images=Images.objects.create(image=i["image"],product_num=product.id)
    #     product.image.add(images)
    #     product.save()     
    # proc_1=Product.objects.create(name="Dji Phantom Drone 4k",price=160,discount_percent=70,branch_id=1,category_id=9,stock=120,details="this is drone")
    # image_1=Images.objects.create(image="https://d2r00w08fz6ft0.cloudfront.net/ludus-demo/images/product/electronic/product11.9408f979aded4474a5450849f8dbc556.jpg",product_num=proc_1.id)
    # proc_1.image.add(image_1)
    # proc_2=Product.objects.create(name="Dji Phantom Drone 2k",price=200,discount_percent=50,branch_id=1,category_id=9,stock=150,details="this is drone")
    # image_2=Images.objects.create(image="https://d2r00w08fz6ft0.cloudfront.net/ludus-demo/images/product/electronic/product12.656532af809b9068d2575bd4fe8a47ba.jpg",product_num=proc_2.id)
    # proc_2.image.add(image_2) 
    context={}       
    return render(request,"test.html",context)

def success(request):
    return render(request,"success.html")

def faq(request):
    questions=FAQ.objects.all()
    context={"questions":questions}
    return render(request,"faq.html",context)
            
def about(request): 
    return render(request,"about.html")

def contact(request):
    if request.is_ajax():    
        name=request.POST.get("name")
        email=request.POST.get("email")    
        subject=request.POST.get("subject")
        message=request.POST.get("message")
        contact=Contact.objects.create(name=name,email=email,subject=subject,message=message)
        data={"id":contact.id}
        return JsonResponse(data)
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


def blogs(request):
    blogs=Blogs.objects.all()
    context={"blogs":blogs}
    return render(request,"blog.html",context)

def my_custom_page_not_found_view(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 404
    return response
  
 

def my_custom_error_view(request, template_name="404.html"):
    response = render(request,template_name)
    response.status_code = 500
    return response
     
def my_custom_permission_denied_view(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 403
    return response

   
def my_custom_bad_request_view(request, exception, template_name="404.html"):
    response = render(template_name)
    response.status_code = 400
    return response
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser)
def dashboard(request):   
    products=Product.objects.all()  
    context={"products":products}
    return render(request,"dashboard/home.html",context)

@user_passes_test(lambda u: u.is_superuser)
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
@user_passes_test(lambda u: u.is_superuser)
def modify_product(request,id):
    product=get_object_or_404(Product,id=id)
    form=ProductForm(request.POST or None ,request.FILES or None,instance=product)
    if form.is_valid():
        form.save()
    context={"form":form,'product':product}
    return render(request,"dashboard/product_modify.html",context)
@user_passes_test(lambda u: u.is_superuser)
def delete_product(request,id):
    product=get_object_or_404(Product,id=id)
    product.delete()
    return redirect(reverse("home:dashboard"))
@user_passes_test(lambda u: u.is_superuser)
def deals(request):
    deals=Deals.objects.all()
    context={"deals":deals}
    return render(request,"dashboard/deals.html",context)
@user_passes_test(lambda u: u.is_superuser)
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
@user_passes_test(lambda u: u.is_superuser)
def deals_delete(request,id):
    deals=Deals.objects.get(id=id)
    deals.delete()
    return redirect(reverse("home:deals"))
@user_passes_test(lambda u: u.is_superuser)
def category_dash(request):
    category=Category.objects.all()
    return render(request,"dashboard/category.html",{"category":category})
@user_passes_test(lambda u: u.is_superuser)   
def category_add(request):
    form =CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse("home:category"))
    context={"form":form}
    return render(request,"dashboard/category_add.html",context)
@user_passes_test(lambda u: u.is_superuser)
def category_delete(request,id):
    category=Category.objects.get(id=id)
    category.delete()
    return redirect(reverse("home:category"))
@user_passes_test(lambda u: u.is_superuser)
def dashboard_branch(request):
    branch=Branch.objects.all()
    return render(request,"dashboard/branch.html",{"branch":branch})
@user_passes_test(lambda u: u.is_superuser)   
def branch_add(request):
    form =BranchForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse("home:branch"))
    context={"form":form}
    return render(request,"dashboard/branch_add.html",context)
@user_passes_test(lambda u: u.is_superuser)
def branch_delete(request,id):
    branch=Branch.objects.get(id=id)
    branch.delete()       
    return redirect(reverse("home:branch"))
@user_passes_test(lambda u: u.is_superuser)
def manu(request):
    manu=Manufacturer.objects.all()
    return render(request,"dashboard/manu.html",{"manu":manu})
@user_passes_test(lambda u: u.is_superuser) 
def manu_add(request):
    form =ManuForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse("home:manu"))
    context={"form":form}
    return render(request,"dashboard/manu_add.html",context)
@user_passes_test(lambda u: u.is_superuser)
def manu_delete(request,id):
    manu=Manufacturer.objects.get(id=id)
    manu.delete()       
    return redirect(reverse("home:manu"))
@user_passes_test(lambda u: u.is_superuser)
def dash_orders(request):
    orders=Order.objects.all().order_by("statue")
    canceled=Order.objects.filter(statue="canceled").count()
    show={}
    if request.method == "POST":
        show=request.POST.get("show")
        if show == "1" or show == 1:
            orders=Order.objects.filter(statue="processing")
            
        if show == "2" or show == 2:
            orders=Order.objects.filter(statue="canceled")
        if show == "3" or show == 3:
            orders=Order.objects.filter(statue="delivered")
        if show == "4" or show == 4:
            orders=Order.objects.filter(statue="shipped")  
    context={"orders":orders,"canceled":canceled,"show":show}   
    return render(request,"dashboard/orders.html",context)
@user_passes_test(lambda u: u.is_superuser)  
def dash_order_details(request,id):
    try:
        orders=Order.objects.get(id=id)
        if request.method == 'POST':
            statue=request.POST.get("statue")
            orders.statue=statue
            orders.save()
            return redirect(reverse("home:dash_orders"))

    except:     
        return redirect(reverse("home:dash_orders"))
    context={"orders":orders}
    return render(request,"dashboard/order_details.html",context)
# def search(request):
#     qs = request.GET.get("q")    
#     product=Product.objects.filter(Q(name__icontains=qs)| Q(category__name__icontains=qs)|Q(branch__child__icontains=qs)|Q(details__icontains=qs)).distinct()
#     paginator = Paginator(product,2)
#     page_num =  request.GET.get("page")
#     page_obj = paginator.get_page(page_num)       
#     return render(request,"search.html")
