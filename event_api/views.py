from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework.generics import ListAPIView
from rest_framework import status,permissions,filters
from datetime import datetime , timedelta
from django.contrib.auth import authenticate ,login , logout
from django.db.models import Q






class Eventfetch(ListAPIView):
  
    permission_classes=(permissions.IsAuthenticated,) 
    queryset = Event.objects.all()
    serializer_class = PostSerializer 
    template_name="index.html"
    filter_backends = [filters.SearchFilter]
    search_fields = ['^slug']

    def get_queryset(self):
        initial_date = Event.objects.first().created_on 
        current_date = datetime.now() - timedelta(days = 1)
        return Event.objects.filter(~Q(start_date__date__range=[initial_date.date(),current_date.date()]))
 
   

class Filterapi(ListAPIView):
    serializer_class = PostSerializer 
    template_name="index.html"
    def get_queryset(self):
        start_date =  datetime.strptime(self.kwargs['startdate'],"%m-%d-%Y")
        end_date =  datetime.strptime(self.kwargs['enddate'],"%m-%d-%Y")
        category = self.kwargs['category'].lower()   
        initial_date = Event.objects.first().created_on 
        current_date = datetime.now() - timedelta(days = 1)
        return Event.objects.filter(Q(start_date__date__range=[start_date.date(),end_date.date()],categories=category) & ~Q(start_date__date__range=[initial_date.date(),current_date.date()]))






class Login(APIView):

    permission_classes=(permissions.AllowAny,)  
    def get(self,request):
        try:      
            return Response(data={"data":"True"},status=status.HTTP_202_ACCEPTED,template_name="register.html")
        except:
            return Response(data={"data":"False","message":"Oops something went wrong !"},status=status.HTTP_202_ACCEPTED)


    def post(self,request):
        try:
            print(request.data)
            username = request.data.get('username')
            password = request.data.get('password')
            data = User.objects.filter(username=username).exists()
            if not data:
                return Response(data={"data":"False","message":"Invalid Username"},status=status.HTTP_202_ACCEPTED)
            data = User.objects.filter(username=username,password=password).exists()
            if data ==  True:
                user = User.objects.get(username=username,password=password)
                login(request, user)
                return Response(data={"data":"True"},status=status.HTTP_202_ACCEPTED)
            return Response(data={"data":"False","message":"Invalid password"},status=status.HTTP_202_ACCEPTED)
        except:
            return Response(data={"data":"False","message":"Oops something went wrong !"},status=status.HTTP_202_ACCEPTED)


class Logout(APIView):
    def post(self,request):
        try:
            logout(request)
            return Response(data={"data":"True"},status=status.HTTP_202_ACCEPTED)
        except:
            return Response(data={"data":"False","message":"Oops something went wrong !"},status=status.HTTP_202_ACCEPTED)


class Createuser(APIView):
    permission_classes=(permissions.AllowAny,)  
    def post(self, request):

        try:
            data = User.objects.filter(username=request.data.get('username')).exists()
            if data:
                return Response(data={"data":"False","message":" User already exists"},status=status.HTTP_202_ACCEPTED)
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(is_staff=True)
                print(serializer.errors)
                return Response(data={"data":"True","message":"User successfully registered please login"},status=status.HTTP_201_CREATED)
            return Response(data={"data":"False","message":"Oops something went wrong !"},status=status.HTTP_202_ACCEPTED)    
        except Exception as e:
            return Response(data={"data":"False","message":"Oops something went wrong !"},status=status.HTTP_202_ACCEPTED)



class Likeapi(APIView):
    def post(self,request):
        try:
            event_id = request.data.get('event_id')
            action = request.data.get('action')
            event_obj = Event.objects.get(id=event_id)
            if action =='like':               
                event_obj.like.add(request.user)
                event_obj.dislike.remove(request.user)
            else:
                event_obj.dislike.add(request.user)
                event_obj.like.remove(request.user)
                  

            return Response(data={"data":"True"},status=status.HTTP_202_ACCEPTED)
        except:
            return Response(data={"data":"False","message":"Oops something went wrong !"},status=status.HTTP_202_ACCEPTED)






            
    



     










