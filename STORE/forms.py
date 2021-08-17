from django import forms
from .models import *
from bootstrap_datepicker_plus import DatePickerInput,TimePickerInput,DateTimePickerInput

# class SignupForm(forms.Form):
#     first_name = forms.CharField(max_length=30, label='Voornaam')
#     last_name = forms.CharField(max_length=30, label='Achternaam')

#     def signup(self, request, user):
#         user.first_name = self.cleaned_data['first_name']
#         user.last_name = self.cleaned_data['last_name']
#         user.save()
class ProductForm(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model=Product
        fields="__all__"
        exclude=["image","stars"]
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        # self.fields["category"].queryset = Type_Child.objects.none()
        if "category" not in self.data:
            self.fields["branch"].queryset = Branch.objects.none()
            # print(self.data)

        # if self.data["type"] == None:
        #     print(self.data["type"],"hi")
        #     self.fields["category"].queryset = Type_Child.objects.filter(type=None) 
       
    
        elif "category" in self.data:
            # print(self.data["category"])
            if self.data["category"] == "":
                self.fields["category"].queryset = Branch.objects.none()

            else:
                self.fields["branch"].queryset = Branch.objects.filter(name__id=self.data["category"])
       


class PriceForm(forms.ModelForm):
    price_1=forms.CharField(max_length=50,required=True)
    price_2=forms.CharField(max_length=50,required=True)
    class Meta:
        model=Product
        fields=["price_1","price_2",]
        
class ManiForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=["manufacturer"]
        
    

class RateForm(forms.ModelForm):
    review=forms.CharField()
    stars=forms.CharField()
    class Meta:
        model=Rate
        fields=["user","review","stars"]
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields="__all__"
        exclude=["user"]
    
class AddressEdit(forms.ModelForm):
    class Meta:
        model=Address
        fields="__all__"
        exclude=["profile","primary"]
    
class DealForm(forms.ModelForm):
    expire_date =forms.DateField(widget=DatePickerInput())
    class Meta:
        model=Deals
        fields="__all__"
        exclude=['expired']
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields="__all__"
    
        
class BranchForm(forms.ModelForm):
    class Meta:
        model=Branch
        fields="__all__"
    
    
        
class ManuForm(forms.ModelForm):
    class Meta:
        model=Branch
        fields="__all__"

from allauth.account.forms import LoginForm,SignupForm
GENDER=(    
    ("Male","Male"),
    ("Female","Female")
)
  
class MyCustomSignupForm(SignupForm):
    last_name=forms.CharField(max_length=10)
   
    def save(self, request):
          
        # Ensure you call the parent class's save.
        # .save() returns a User object.
        user = super(MyCustomSignupForm, self).save(request)
        first_name=request.POST.get("username")
        last_name=self.cleaned_data.get("last_name")
        user.first_name=first_name      
        user.last_name=last_name
        user.save()    
       
        phone=request.POST.get("phone")
        gender=request.POST.get("gender")
        year=request.POST.get("year")
        month=request.POST.get("month")
        day=request.POST.get("day")
        birthday=f"{year}-{month}-{day}"
        profile=Profile.objects.get(user_id=user.id)
        profile.phone=phone
        profile.gender=gender
        profile.birthday=birthday
        profile.save()
        # if profile.phone == None or profile.gender == None or profile.birthday == None:
        #     raise forms.ValidationError("invalid Data")
        # Add your own processing here.

        # You must return the original result.
        return user
