from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Category(models.Model):
    name=models.CharField(max_length=100) 
   
    def same_category(self):
        branch=Branch.objects.filter(name__name=self.name)   
        return branch
    def my_products(self):       
        product=Product.objects.filter(branch__name=self.id)
        return product

    def __str__(self):                                  
        return self.name     

class Branch(models.Model):
    name=models.ForeignKey(Category,default=1,on_delete=models.CASCADE)
    child=models.CharField(max_length=100)
    def __str__(self):                                  
        return self.name.name
 
    def same_category(self):
        cat= Branch.objects.filter(name=self.name)[0:4]
        return cat

        return product
class Manufacturer(models.Model):
    name=models.CharField(max_length=100)

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
        return str(self.product_num)      
    # def save(self,*args, **kwargs):
    #     self.image = self.name
    #     super(Images,self).save(*args, **kwargs)
         
class Product(models.Model):
    name=models.CharField(max_length=100)  
    image=models.ManyToManyField(Images)
    free_shipping=models.BooleanField(default=False)
    price=models.PositiveIntegerField(default=0)
    details=models.TextField()
    category=models.ForeignKey(Category,default=1,null=True,on_delete=models.SET_NULL)
    branch=models.ForeignKey(Branch,default=1,null=True,on_delete=models.SET_NULL)
    manufacturer=models.ForeignKey(Manufacturer,null=True,default=1,on_delete=models.SET_NULL)
    color=models.ForeignKey(Color,default=1,null=True,on_delete=models.SET_NULL)
    size=models.ManyToManyField(Size,blank=True)    
    
    def __str__(self):                                         
        return self.name
 
    def free_ship(self):
        return Product.objects.filter(price__range=(200,1000))

class Rate(models.Model):
   my_product=models.ForeignKey(Product,default=1,blank=True,on_delete=models.CASCADE)   
   
   def __str__(self):                                  
        return self.product.name
    
class Filter(models.Model):
    user=models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    category=models.ForeignKey(Category,blank=True,null=True,on_delete=models.CASCADE)
    rating=models.ForeignKey(Rate,blank=True,null=True,on_delete=models.CASCADE)
    shipping=models.BooleanField(default=False)
    price_1=models.PositiveIntegerField(default=1,blank=True,null=True)
    price_2=models.PositiveIntegerField(default=200,blank=True,null=True)
    manufacturer=models.ForeignKey(Manufacturer,blank=True,null=True,on_delete=models.CASCADE)
    color=models.ForeignKey(Color,default=1,blank=True,null=True,on_delete=models.CASCADE)
    size=models.ForeignKey(Size,blank=True,null=True,on_delete=models.CASCADE)
    device=models.CharField(max_length=200)
    show=models.PositiveIntegerField(default=0)
    sort=models.PositiveIntegerField(default=0)
    def __str__(self):   
        try:
            name=self.user.username  
        except:
            name=str(self.id)                       
        return name  
    
class Product_Cart(models.Model):
    user=models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    products=models.ForeignKey(Product,blank=True,null=True,on_delete=models.CASCADE)
    product_id=models.CharField(max_length=200)

    price=models.PositiveIntegerField(default=0)
    ordered=models.BooleanField(default=False)
    delivered=models.BooleanField(default=False)
    device=models.CharField(max_length=200)
    def __str__(self):
        
        return self.products.name    
    def products_cart(self):   
        products=Product.objects.filter(products_id=self.products)
        print(products)
        return products
class Cart(models.Model):
    user=models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    products=models.ManyToManyField(Product_Cart,blank=True)
    device=models.CharField(max_length=200)
    ordered=models.BooleanField(default=False)
    delivered=models.BooleanField(default=False)

    def __str__(self):
        try:
            name=self.user.username
        except:
           name=str(self.id) 
        return name


      
class Wishlist(models.Model):
    user=models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    products=models.ManyToManyField(Product,blank=True)
    device=models.CharField(max_length=200)

    def __str__(self):
        try:
            name=self.user.username
        except:
           name=str(self.id) 
        return name

