from .models import *
from django.core.paginator import Paginator

def global_context(request):
    category=Category.objects.all() 

    mani=Manufacturer.objects.all()
    color=Color.objects.all()
    size=Size.objects.all()
    branch=Branch.objects.all()
    if request.user.is_authenticated:
        wishlist=Wishlist.objects.get_or_create(user=request.user)
    else:
        try:
            device=request.COOKIES["device"]
        except:
            wishlist=[]
            pass
        wishlist=Wishlist.objects.get_or_create(device=device)

   
       
    context={"wishlist":wishlist,"color":color,"size":size,"category":category,"mani":mani,"branch":branch,}
    return context           
