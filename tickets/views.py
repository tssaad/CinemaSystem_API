import re
from django.http import response
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.fields import MISSING_ERROR_MESSAGE
from . models import *
from .serializers import *

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics, mixins, viewsets
from django.http import Http404

# 1) no model no REST
def test(request):
    guests = [
        {
            'id': 1,
            'name': 'Test',
            'phone': 1234,
        },

        {
            'id': 2,
            'name': 'Test2',
            'phone': 12342,
        },
    ]
    return JsonResponse(guests, safe=False)

# 2) no rest and from model
def test2(request):
    data = Guest.objects.all()
    response = {
        'guests' : list(data.values())
    }

    return JsonResponse(response, safe=False)

#3 Fuction based view
#3.1 GET and POST
@api_view(['GET', 'POST'])
def FBV_list(request):
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            #1 can also send the whole list
            #guests = Guest.objects.all()
            #serializer = GuestSerializer(guests, many=True)
            #return Response(serializer.data)
            # 2 can also send the new added data only
            return Response(serializer, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

#3.2 GET_pk, PUT, DELETE
@api_view(['GET','PUT','DELETE'])
def FBV_pk(request, pk):
    try:
        guest=Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# 4 class based view
# 4.1 GET and POST
class CBVList(APIView):
    def get(self, request):
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

#4.2 GET_pk, PUT, DELETE
class CBV_pk(APIView):
    def get_object(self, pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)

    def put(self, request, pk):
        guest = self.get_object(pk)
        serializer = GuestSerializer(guest, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        guest = self.get_object(pk)
        guest.delete()
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# 5 mixins
# 5.1 mixins list and create
class MixinsList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

# 5.1 mixins get_pk, update and delete
class Mixins_pk(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.destroy(request)

# 6 generics
# 6.1 get and post
class GenericsList(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

# 6.2 others
class Generics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

# 7 viewsets
class ViewsetsGuest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class ViewsetsMovie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    #filter_backends = [filters.SearchFilter]
    #search_fields = ['movie']

class ViewsetsReservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = RevervationSerializer


#8 find movie by function
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        #hall = request.data['hall'],
        movie = request.data['movie'],
    )
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def make_reservation(request):
    movie = Movie.objects.get(movie = request.data['movie'])
    
    guest = Guest()
    guest.name = request.data['name']
    guest.phone = request.data['phone']
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()

    return Response(status=status.HTTP_201_CREATED)

