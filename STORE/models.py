from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from cities_light.models import City
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from google_currency import convert
import json  
from django_countries.fields import CountryField
from cities_light.models import Country,Region,City
from django.shortcuts import render,redirect,reverse
import requests
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
from django.conf import settings

GENDER=(   
    ("Male","Male"),    
    ("Female","Female")
)        
        
@receiver(post_save, sender=User)
def create_user_Customer(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

class Profile(models.Model):  
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=100)
    birthday=models.DateField(auto_now_add=False,null=True)
    gender=models.CharField(choices=GENDER,max_length=20)
    class Meta:      
        verbose_name="Profile"
              
    def __str__(self):
        return self.user.username
    
   
class Category(models.Model):
    name=models.CharField(max_length=100) 
   
    def same_category(self):
        branch=Branch.objects.filter(name__name=self.name)   
        return branch
    def my_products(self):       
        product=Product.objects.filter(category__id=self.id)[0:6]
        return product

    def __str__(self):                                  
        return self.name     

class Branch(models.Model):
    name=models.ForeignKey(Category,default=1,on_delete=models.CASCADE)
    child=models.CharField(max_length=100)
    def __str__(self):                                  
        return self.child
 
    def same_category(self):
        cat= Branch.objects.filter(name=self.name)[0:4]
        return cat

    def my_products(self):       
        product=Product.objects.filter(branch__id=self.id)
        return product
class Manufacturer(models.Model):
    name=models.CharField(max_length=100)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    def __str__(self):                                  
        return self.name
    def my_products(self):       
        product=Product.objects.filter(manufacturer=self.id)
        return product
class Color(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):                                         
        return self.name      
    def my_products(self):       
        product=Product.objects.filter(color=self.id)
        return product
class Size(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):                                  
        return self.name              
    def my_products(self):       
        product=Product.objects.filter(size=self.id)
        return product
    

    
def image_upload(instance, filename):
    # imagename,extension=filename.split(".")
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return (f"products/{instance.product_num}/{filename}")
    # return 'user_{0}/{1}'.format(instance.name, filename)
     
class Images(models.Model):   
    image=models.ImageField(blank=True,upload_to=image_upload)
    product_num=models.PositiveIntegerField(default=0,null=True)        
    # name=models.CharField(max_length=100)   
    def __str__(self):                                          
        return str(self.id)      
    # def save(self,*args, **kwargs):
    #     self.image = self.name
    #     super(Images,self).save(*args, **kwargs)
          


class Product(models.Model):
    name=models.CharField(max_length=100)  
    image=models.ManyToManyField(Images)
    free_shipping=models.BooleanField(default=False)
    price=models.PositiveIntegerField(default=0)
    details=models.TextField()
    stars=models.FloatField(default=0)
    most_buy=models.PositiveIntegerField(default=0)    
    category=models.ForeignKey(Category,default=1,null=True,on_delete=models.SET_NULL)
    branch=models.ForeignKey(Branch,default=1,null=True,on_delete=models.SET_NULL)
    manufacturer=models.ForeignKey(Manufacturer,null=True,blank=True,on_delete=models.SET_NULL)
    color=models.ManyToManyField(Color,blank=True)
    size=models.ManyToManyField(Size,blank=True)    
    stock=models.PositiveIntegerField()
    discount_percent=models.PositiveIntegerField(blank=True,default=0)
    discount_date=models.DateTimeField(blank=True,auto_now_add=False,null=True)
    def __str__(self):                                         
        return self.name
    def comments(self):     #this is to count comments per every product 
        comments=Rate_Details.objects.filter(product_id=self.id).count()
        return comments   
    def average(self):          #this is to calculate average rate for every product   
        average=0
        stars=0
        rates=Rate_Details.objects.filter(product_id=self.id)
        for i in rates:
            stars +=i.stars
            average=stars/len(rates)
        if 1 < average < 2:
            my_average =True
        elif 2 < average < 3:
            my_average =True
        elif 3 < average < 4:    
            my_average =True
        elif 4 < average < 5:
           
            my_average=True
        else:
            my_average=False
        context={"average":average,"my_average":my_average}
        return context

    
    def discount(self):  #this is to calculate discount after percent
        if self.discount_percent != 0:
            disc=(self.discount_percent/100) * self.price 
            price= int(self.price) - disc
        else:
            price=self.price            
        return price 
    
class Rate(models.Model):      
   product=models.ManyToManyField(Product,blank=True)   
   user=models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)

   def __str__(self):                                  
        return self.user.username

class Rate_Details(models.Model):
    rate=models.ForeignKey(Rate,blank=True,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,blank=True,on_delete=models.CASCADE)
    review=models.TextField()
    stars=models.FloatField(default=0)
    date=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.rate.user.username
    def average(self):          #this is to calculate average rate for every product   
        float_star=self.stars
        star_float=False  
        if 1 < float(float_star) < 2:
            star_float=True
        if 2 < float(float_star) < 3:
            star_float=True
        if 4 < float(float_star) < 4:
            star_float=True               
        return star_float
    def ajax_len(self):
        return Rate_Details.objects.filter(product=self.product).count()
class Filter(models.Model):
    user=models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,blank=True,null=True,on_delete=models.CASCADE)
    rating=models.FloatField(default=0)
    shipping=models.BooleanField(default=False)
    price_1=models.PositiveIntegerField(blank=True,null=True)
    price_2=models.PositiveIntegerField(blank=True,null=True)
    manufacturer=models.ForeignKey(Manufacturer,blank=True,null=True,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,blank=True,null=True,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,blank=True,null=True,on_delete=models.CASCADE)
    device=models.CharField(blank=True,null=True,max_length=200)
    show=models.PositiveIntegerField(default=8)
    sort=models.PositiveIntegerField(default=0)
    def __str__(self):   
        try:
            name=self.user.username  
        except:
            name=str(self.id)                       
        return name  
    def star_loop(self):              
        for i in range(int(self.rating)):
            loop =i
            loop +=1        
        if self.rating == 1.5 or self.rating == 2.5 or self.rating == 3.5 or self.rating == 4.5:
            my_loop=True
        else:
            my_loop =False
        print(loop)
        context={"my_loop":my_loop,"loop":loop}
        return context   
class Product_Cart(models.Model):
    user=models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    products=models.ForeignKey(Product,blank=True,null=True,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    size=models.ForeignKey(Size,default=1,null=True,on_delete=models.SET_NULL)
    color=models.ForeignKey(Color,default=1,null=True,on_delete=models.SET_NULL)
    price=models.PositiveIntegerField(default=0)
    ordered=models.BooleanField(default=False)
    delivered=models.BooleanField(default=False)
    modified_date = models.DateTimeField(auto_now=True)
    device=models.CharField(blank=True,null=True,max_length=200)
    def __str__(self):
        
        return self.products.name    
    def products_cart(self):   
        products=Product.objects.filter(products_id=self.products)
        print(products)
        return products
    
    def discount(self):
        if self.products.discount_percent != 0:
            disc=(self.products.discount_percent/100) * self.products.price *self.quantity
            price= int(self.products.price) - disc
        else:
            price=self.products.price * self.quantity          
        return price   
    def product_price_individual(self):
        if self.products.discount_percent != 0:
            disc=(self.products.discount_percent/100) * self.products.price *self.quantity
            price= int(self.products.price) - disc
        else:
            price=self.products.price           
        return price 
    def same_pro(self):
        pro= Product_Cart.objects.filter(user=self.user,ordered=True,delivered=False,products__name=self.products.name)
        # pro=Product.objects.filter(id__in=)
            # print(i)   
        return pro 

    def get_url(self): 
        if settings.DEBUG == False: 
            url=f"https://ludus-ecommerce.herokuapp.com/product/{self.products.id}/"
        else:
            url=f"http://127.0.0.1:8000/product/{self.products.id}/"
        return url   
    def get_category_url(self):
        if settings.DEBUG == False:
            url=f"https://ludus-ecommerce.herokuapp.com/category/{self.products.category.name}/"
        else:
            url=f"http://127.0.0.1:8000/category/{self.products.category.name}/"

        return url   
    def get_cart_remove_url(self):  
        if settings.DEBUG == False:
            url=f"https://ludus-ecommerce.herokuapp.com/remove-from-cart/{self.id}/"
        else:
            url=f"http://127.0.0.1:8000/remove-from-cart/{self.id}/"
        return url   
class Shipping(models.Model):
    country=models.CharField(max_length=50,blank=True,null=True)
    amount=models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.country

class Cart(models.Model):                       
    user=models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    products=models.ManyToManyField(Product_Cart,blank=True)
    modified_date = models.DateTimeField(auto_now=True)
    device=models.CharField(blank=True,null=True,max_length=200)
    price=models.FloatField(default=0)
    shipping=models.ForeignKey(Shipping,blank=True,null=True,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    delivered=models.BooleanField(default=False)
    class Meta:
        ordering=("-modified_date",)   
    def __str__(self):     
        try:
            name=self.user.username
        except:    
           name=str(self.id)     
        return name        
    def order_product_length(self):
        count=0
        for i in self.products.all():
            count=len(self.products.all())
        return count  
    def before_discount(self):
        price=0       
        for i in self.products.all(): 
            price +=i.discount()
        return price 
    def total_price(self):
        price=0   
        for i in self.products.all(): 
            price +=i.discount()
        order=Order.objects.filter(user=self.user,ordered=True,delivered=False)
        if order.exists():
            my_order=Order.objects.get(user=self.user,cart_id=self.id,ordered=True,delivered=False)
            if my_order.address:
                address=Address.objects.get(profile__user=self.user,primary=True)
                shipping=Shipping.objects.get(country=address.country.name)
                price +=shipping.amount
                my_order.price =price
                my_order.save()
        return price      
    def order_shipping(self):
        price=0
        try:
            order=Order.objects.get(user=self.user,delivered=False,ordered=True)
            if order.address:
                address=Address.objects.get(profile__user=self.user,primary=True)
                shipping=Shipping.objects.get(country=address.country.name)
                price=shipping.amount
        except:
            price=0
        return price
    def shipping_price(self):
        price=0   
        for i in self.products.all(): 
            price +=i.discount()
        if self.shipping:
            price += self.shipping.amount 
        return price 
CHOICES=(   
    ("processing","processing"),
    ("shipped","shipped"),
    ("delivered","delivered"),
    ("canceled","canceled")
         )
PAYMENTS=(
    ('Cash on Delivery',"Cash on Delivery"),
    ("PayPal","PayPal"),
    ("Credit / Debit Card","Credit / Debit Card")
)   
class Address(models.Model):
    profile=models.ForeignKey(Profile,on_delete=models.CASCADE)
    phone=models.CharField(max_length=50)
    country=models.ForeignKey(Country,null=True,on_delete=models.CASCADE)
    region=models.ForeignKey(Region,null=True,on_delete=models.CASCADE)
    city=models.ForeignKey(City,on_delete=models.CASCADE)
    street=models.CharField(max_length=300)
  
    zip=models.CharField(max_length=100)
    primary=models.BooleanField(default=False)
    def __str__(self):
        return str(self.id)     
class Coupon(models.Model):
    coupon=models.CharField(unique=True,max_length=20)
    expire_date=models.DateField(auto_now_add=False)
    numbers=models.PositiveIntegerField(default=0)
    value=models.PositiveIntegerField(default=0,validators=[MaxValueValidator(100)])
    def __str__(self): 
        return self.coupon
class Order(models.Model):
    user=models.ForeignKey(User,blank=True,on_delete=models.SET_NULL,null=True)
    cart=models.ForeignKey(Cart,on_delete=models.SET_NULL,null=True)
    price=models.FloatField(default=0)
    egy_currency=models.IntegerField(default=0)
    track_number=models.CharField(max_length=2000)
    ordered=models.BooleanField(default=False)   
    delivered=models.BooleanField(default=True)
    order_date=models.DateTimeField(auto_now_add=True)
    statue=models.CharField(choices=CHOICES,default="processing",max_length=100)
    coupon=models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank=True)
    notes=models.TextField(blank=True)
    address=models.ForeignKey(Address,on_delete=models.SET_NULL,null=True)
    payments=models.CharField(choices=PAYMENTS,max_length=100)
    device=models.CharField(blank=True,null=True,max_length=1000)
   
    def __str__(self):         
        user=str(self.id)   
        return user
    # def converter(self):
    #     converter=json.loads(convert('usd', 'egp', self.price)) #to transefer to JSON data
    #     price=int(float(converter["amount"]))
    #     total=round(price)
    #     return total   
    def converter(self):
        try:
            api=requests.get("http://api.currencylayer.com/live?access_key=bbd4b1fcbe13b2bf0b8a008bc1daa606&currencies=EGP&format = 1")
            price=api.json()
            for i in price["quotes"]: 
                pass 
            money=price["quotes"][i] * self.price
            total=round(money)
            self.egy_currency=total
            self.save()
           
        except:
            total=None
        return total   
    def get_absolute_order(self):    
        if settings.DEBUG == False:
            url=f"https://ludus-ecommerce.herokuapp.com/order/user/{self.user}/"
        else:
            url=f"http://127.0.0.1:8000/order/user/{self.user}/"
        return url
    def order_total(self):
        price=self.cart.total_price()
        if self.coupon:
            coupon=self.coupon.value
            money=price - ((coupon / 100) * price) 
            price =money
            self.price =price
            self.save()
        return price
    def shipping(self):
        try:
            ship =Shipping.objects.get(country=self.address.country.name)
        except:
            ship=None
        return ship
class Wishlist(models.Model):     
    user=models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    products=models.ManyToManyField(Product,blank=True)
    modified_date = models.DateTimeField(auto_now=True)

    device=models.CharField(max_length=200)

    def __str__(self):
        try:   
            name=self.user.username
        except:
           name=str(self.id) 
        return name
    def product_length(self):
        num=self.products.count()
        print(num)
        return num

class FAQ(models.Model):
    question=models.CharField(max_length=200)
    answer=models.TextField()

    def __str__(self):
        return self.question

class Contact(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField(max_length=50)
    subject=models.CharField(max_length=50)
    message=models.TextField()

    def __str__(self):
        return self.name

class NewsLetter(models.Model):
    user=models.ManyToManyField(User,blank=True)
    device=models.CharField(max_length=500)

    def __str__(self):
        try:
            name=self.user.username
        except:
            name=self.device
        return name
        
       
class Deals(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    expire_date=models.DateTimeField(auto_now_add=False)
    expired=models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)



def blog_image_upload(instance, filename):
    # imagename,extension=filename.split(".")
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return (f"blogs/{instance.blog}/{filename}")
    # return 'user_{0}/{1}'.format(instance.name, filename)
  
class Blog_Category(models.Model):
    name=models.CharField(max_length=100)
    def __Str__(self):
        return self.name
    
class Blog_Comments(models.Model): 
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    details=models.TextField()
    date_created=models.DateTimeField(auto_now_add=True)
    blog_num=models.PositiveIntegerField(default=0)
    def __str__(self):
        try:
            num=Blogs.objects.get(id=self.blog_num)
            return num.title
        except:
            return self.blog_num
class Blog_Images(models.Model):
    blog_num=models.PositiveIntegerField(default=0)
    image=models.ImageField(null=True,upload_to=blog_image_upload)
    
    def __str__(self):
        try:
            num=Blogs.objects.get(id=self.blog_num)
            return num.title
        except:
            return self.blog_num
class Blogs(models.Model):
    title=models.CharField(max_length=100)
    details=RichTextUploadingField()
    category=models.ForeignKey(Blog_Category,on_delete=models.SET_NULL,null=True)
    image=models.ManyToManyField(Blog_Images,blank=True)
    date=models.DateTimeField(auto_now_add=True)
    hashtag=models.CharField(max_length=150)
    comments=models.ManyToManyField(Blog_Comments,blank=True)

    def __str__(self):
        return self.title    