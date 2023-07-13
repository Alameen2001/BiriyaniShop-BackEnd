from django.contrib.auth.models import User
from api.models import Biriyani,Cart,Order,Review
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','email','password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    

class ReviewSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    biriyani=serializers.CharField(read_only=True)
    class Meta:
        model=Review
        fields='__all__'

class BiriyaniSerializer(serializers.ModelSerializer):
    category=serializers.StringRelatedField()
    reviews=ReviewSerializer(read_only=True,many=True)
    class Meta:
        model=Biriyani
        fields='__all__'

class CartSerializer(serializers.ModelSerializer):
    biriyani=BiriyaniSerializer(read_only=True)
    user=serializers.CharField(read_only=True)
    date=serializers.CharField(read_only=True)
    status=serializers.CharField(read_only=True)


    class Meta:
        model=Cart
        fields='__all__'

class OrderSerializer(serializers.ModelSerializer):
    biriyani=BiriyaniSerializer(read_only=True)
    user=serializers.CharField(read_only=True)
    class  Meta:
        model=Order
        fields='__all__'

# class 

