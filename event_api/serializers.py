from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from rest_framework.authtoken.views import Token
from rest_framework.fields import CurrentUserDefault



class PostSerializer(serializers.ModelSerializer):
    start_dates = serializers.DateTimeField(source="start_date",format="%d-%m-%y")
    end_dates = serializers.DateTimeField(source="end_date",format="%d-%m-%y")
    start_time = serializers.DateTimeField(source="start_date",format="%H:%M %p")
    end_time = serializers.DateTimeField(source="end_date",format="%H:%M %p")
    # liked = serializers.SerializerMethodField()
    # disliked = serializers.SerializerMethodField()
    


    class Meta:
        fields = ['id', 'title','image','description','location',"start_time","end_time",'start_dates','end_dates','categories','published','paid']
        model = Event

    # def get_liked(self,obj):
    #     a = serializers.CurrentUserDefault()
    #     print(a)
    #     return Event.objects.filter(id=obj[0].id,like=serializers.CurrentUserDefault()).exists()

    # def get_disliked(self,obj):
    #     return Event.objects.filter(id=obj[0].id,like=serializers.CurrentUserDefault()).exists()






class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

        extra_kwargs = {'password':{
            'write_only':True,
            'required':True
        }}




