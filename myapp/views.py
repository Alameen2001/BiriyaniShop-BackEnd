from django.shortcuts import render,redirect
from django.views.generic import CreateView,View,FormView,ListView,DetailView,DeleteView
from myapp.forms import BiriyaniForm
from api.models import Biriyani,Category,Order,Review,User
from django.contrib.auth.models import User
from myapp.forms import RegistationForm,LoginForm
from django.urls import reverse_lazy
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.views import LogoutView
from datetime import date
from django.db.models import Count, Sum




class SignUpView(CreateView):
    model=User
    template_name="register.html"
    form_class=RegistationForm
    success_url=reverse_lazy("signin")

class SignInView(FormView):
    form_class=LoginForm
    template_name="myapp/login.html"
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr and usr.is_superuser:
                login(request,usr)
                return redirect("biri-add")
            else:
                print ("not working")
                return render(request,self.template_name,{"form":form})
            
class SignOutView(LogoutView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")
            

            

class BiriyaniCreateView(CreateView):
    template_name="biri-add.html"
    def get(self,request,*args,**kwargs):
        form=BiriyaniForm()
        return render (request,self.template_name,{"form":form})
    def post(self,request,*args,**kwargs):
        form=BiriyaniForm(request.POST)
        if form.is_valid():
            form.save()
            print('data saved')
            return redirect("biri-list")
           

        else:
             return render(request,"myapp/biri-list.html",{form:form})
        


class BiriyaniListView(ListView):
    model=Biriyani
    template_name="myapp/biri-list.html"
    context_object_name="biriyani"

    def get_queryset(self):
        return Biriyani.objects.all()

    def get(self,request,*args,**kwargs):
        qs=self.get_queryset()
        return render(request,self.template_name,{"biriyani":qs})




class BiriyaniDetailView(DetailView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Biriyani.objects.get(id=id)
        return render(request,"myapp/biri-detail.html",{"biriyani":qs})


class BiriyaniDeleteView(DeleteView):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Biriyani.objects.get(id=id).delete()
        return redirect("biri-list")

class BiriyaniEditView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Biriyani.objects.get(id=id)
        form=BiriyaniForm(instance=obj)
        return render(request,"myapp/biri-edit.html",{"form":form})

    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Biriyani.objects.get(id=id)
        form=BiriyaniForm(request.POST,instance=obj,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect("biri-list")
        else:
            return render(request,"biri-edit.html",{"form":form})
        

        




    



def dashboardView(request, *args, **kwargs):
    # Get the dates and corresponding product sold amounts
    dates_products_sold = Order.objects.values('date').annotate(
        total_products_sold=Count('id'),
        total_products_sum=Sum('biriyani__price'),
        total_users=Count('user', distinct=True)
    ).order_by('date')

    # Get the total number of products sold
    total_products_sold =None
    total_products_sum=None
    total_users=None

     # Get the total number of products sold
    total_products_sold = Order.objects.count()

    
    # Get the total amount of biriyani sold
    total_biriyani_sold = Order.objects.aggregate(total_amount=Sum('biriyani__price'))

    # Get the total number of registered users
    total_users_registered = User.objects.count()

    # Get the number of users who ordered till now
    users_ordered_total = User.objects.filter(order__isnull=False).distinct().count()

    # Get the total number of reviews
    total_reviews = Review.objects.count()

    # Get the total number of comments
    total_comments = Review.objects.aggregate(total_count=Count('comment'))['total_count']


    reviews = Review.objects.select_related('user').order_by('-date')

     # Retrieve specific information about the users who placed orders
    orders = Order.objects.select_related('user').order_by('-date')

 
   

    context = {
        'dates_products_sold': dates_products_sold,
        'total_products_sold': total_products_sold,
        'dates_products_sold': dates_products_sold,
        'total_products_sum':total_products_sum,
        'reviews': reviews,
        'total_users':total_users,
        'users_ordered_total': users_ordered_total,
        'total_biriyani_sold': total_biriyani_sold['total_amount'] if total_biriyani_sold['total_amount'] else 0,
        'total_users_registered': total_users_registered,
        'total_reviews': total_reviews,
        'total_comments': total_comments,
        'orders': orders
        
    }

    return render(request, 'myapp/dashboard.html', context)
        





        

            

