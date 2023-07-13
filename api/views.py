from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import action
from rest_framework import mixins
from rest_framework import authentication,permissions
from api.serializers import UserSerializer,BiriyaniSerializer,CartSerializer,OrderSerializer,ReviewSerializer
from api.models import Biriyani,Cart,Order,Category,Review


class UsersView(viewsets.GenericViewSet,mixins.CreateModelMixin):
    serializer_class=UserSerializer
    queryset=User.objects.all()



class BiriyaniView(viewsets.GenericViewSet,mixins.ListModelMixin,mixins.RetrieveModelMixin):
    serializer_class=BiriyaniSerializer
    queryset=Biriyani.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]


    def get_queryset(self):
        qs=Biriyani.objects.all()
        if "category" in self.request.query_params:
            cat=self.request.query_params.get("category")
            print(cat)
            qs=qs.filter(category__name=cat)
            print(qs)
        print("out",qs)
        return qs




#   url:'http://127.0.0.1:8000/api/biriyani/:id/add_to_cart/' 
    @action(methods=['POST'],detail=True)
    def add_to_cart(self,request,*args,**kwargs):
        serializer=CartSerializer(data=request.data)
        biriyani_obj=Biriyani.objects.get(id=kwargs.get('pk'))
        user=request.user
        if serializer.is_valid():
            serializer.save(biriyani=biriyani_obj,user=user)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    
#  url:'http://127.0.0.1:8000/api/biriyani/:id/place_order/' 
    @action(methods=['POST'],detail=True)
    def place_order(self,request,*args,**kwargs):
        serializer=OrderSerializer(data=request.data)
        biriyani_obj=Biriyani.objects.get(id=kwargs.get('pk'))
        user=request.user
        if serializer.is_valid():
            serializer.save(biriyani=biriyani_obj,user=user)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    



#   url:'http://127.0.0.1:8000/api/biriyani/:id/add_review/' 
    @action(methods=['POST'],detail=True)
    def add_review(self,request,*args,**kwargs):
        serializer=ReviewSerializer(data=request.data)
        biriyani_obj=Biriyani.objects.get(id=kwargs.get('pk'))
        user=request.user
        if serializer.is_valid():
            serializer.save(biriyani=biriyani_obj,user=user)
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
    @action(methods=["get"],detail=False)       
    def categories(self,request,*args,**kwargs):
        cats=Category.objects.values_list("name",flat=True)
        return Response(data=cats) 


 
      
            






        
  

class CartsView(viewsets.GenericViewSet,mixins.ListModelMixin):
    serializer_class=CartSerializer
    queryset=Cart.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
class OrdersView(viewsets.ModelViewSet,mixins.ListModelMixin):
    serializer_class=OrderSerializer
    queryset=Order.objects.all()
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    @action(methods=['delete'],detail=True)
    def cancel_order(request,*args,**kwargs):
        order_id=kwargs.get("pk")
        try:
            order=Order.objects.get(id=order_id)
            order.delete()
            return Response({'message':'Order canceled successfully.'})
        except Order.DoesNotExist:
            return Response({'error':'Order not found.'},status=404)
        




    


