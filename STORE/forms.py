from django import forms
from .models import *


class ProductForm(forms.ModelForm):
    image = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    class Meta:
        model=Product
        fields="__all__"
        exclude=["image"]
    
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
        
    

 
    
    