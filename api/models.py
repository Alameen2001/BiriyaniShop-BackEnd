from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator,MaxValueValidator


# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=200,unique=True)

    def __str__(self) -> str:
        return self.name
    
class Biriyani(models.Model):
    name=models.CharField(max_length=200)
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    options=(
        ('half','half'),
        ('full','full')
        )
    quantity=models.CharField(max_length=200,choices=options,default='full')
    options=(
         ('in cart','in cart'),
         ('order placed','order placed'),
         ('order cancelled','order cancelled')
    )
    status=models.CharField(max_length=200,choices=options,default='in cart')
    price=models.FloatField()
    image=models.ImageField(upload_to='images',blank=True,null=True)
     
    @property 
    def reviews(self):
        return Review.objects.filter(biriyani=self)

    def __str__(self) -> str:
            return self.name 
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    biriyani=models.ForeignKey(Biriyani,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    options=(
         ('in cart','in cart'),
         ('order placed','order placed'),
         ('order cancelled','order cancelled')
    )
    status=models.CharField(max_length=200,choices=options,default='in cart')

class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    biriyani=models.ForeignKey(Biriyani,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    address=models.CharField(max_length=300)

class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    biriyani=models.ForeignKey(Biriyani,on_delete=models.CASCADE)
    date=models.DateField(auto_now_add=True)
    comment=models.TextField(max_length=200)
    rating=models.FloatField(validators=[MinValueValidator(1),MaxValueValidator(5)]) 

    def _str_(self) -> str:
         return self.comment