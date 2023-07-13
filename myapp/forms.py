from django import forms
from api.models import Biriyani
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistationForm(UserCreationForm):

    class Meta:
        model=User
        fields=["username","password1","password2"]

        widgets={
        "username" : forms.TextInput(attrs={"class":"form-control" }),
        "password1" : forms.TextInput(attrs={"class":"form-control" }),
        "password2" : forms.PasswordInput(attrs={"class":"form-control" }),
  
    }

class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))



 
class BiriyaniForm(forms.ModelForm):
    class Meta:
        model=Biriyani
        fields=[
            "name",
            "category",
            "quantity",
            "price",
            "image"
        ]
 
 