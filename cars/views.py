import json
from datetime import date
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse,JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view,parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from cars import serializer
from cars.serializer import CarSerializer,CustomerSerializer,AvailableCarSerializer,ReservationSerializer
from cars.models import Car,Customer,Reservation
# Create your views here.

#demo check
def hello(request):
    return HttpResponse("hello")

#home page response
@api_view(['GET'])
def home(request):
    if request.method=="GET":
        data=[{'message':'Welcome to Car Reservation system'}]
        return JsonResponse(data,safe=False)
    
@api_view(['GET'])
def view_all_customer(request):
    """
    Its Consits of all customer list
    """
    
    if request.method=="GET":
        customers=Customer.objects.all()
        serializer=CustomerSerializer(customers,many=True)
        return Response(serializer.data)
    
@api_view(['GET'])   
def customer_details(request,cust_pk):
    """
    API to specific customer details
    """
    try:
        customer=Customer.objects.get(pk=cust_pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method=="GET":
        serializer=CustomerSerializer(customer)
        return Response(serializer.data)
    
@api_view(['POST'])
def add_customer(request):
    """
    API for add customer 
    """
    
    if request.method=="POST":
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['PUT'])
def update_customer_details(request,cust_pk):
    """
    API for update customer details
    """
    
    try:
        customer = Customer.objects.get(pk=cust_pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CustomerSerializer(customer, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_customer(request, cust_pk):
    """
    API endpoint for deleting customer details.
    """
    try:
        customer = Customer.objects.get(pk=cust_pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        customer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def view_all_cars(request):
    """
    Its Consits of all cars list
    """
    
    if request.method=="GET":
        cars=Car.objects.all()
        serializer=CarSerializer(cars,many=True)
        return Response(serializer.data)

@api_view(['GET'])   
def car_details(request,car_pk):
    """
    API to specific Car details
    """
    try:
        car=Car.objects.get(pk=car_pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method=="GET":
        serializer=CarSerializer(car)
        return Response(serializer.data)

@api_view(['POST'])
def add_car(request):
    """
    API for Car customer 
    """
    
    if request.method=="POST":
        serializer = CarSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  

@api_view(['PUT'])
def update_car_details(request,car_pk):
    """
    API for update Car details
    """
    
    try:
        car = Car.objects.get(pk=car_pk)
    except Customer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = CarSerializer(car, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_car(request, car_pk):
    """
    API endpoint for deleting car details.
    """
    try:
        car = Car.objects.get(pk=car_pk)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def view_all_reservations(request):
    """
    API endpoint for showing all reservations in the system.
    """
    if request.method == 'GET':
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def view_reservation_details(request, rent_pk):
    """
    API endpoint for showing a particular reservation details.
    """
    try:
        reservation = Reservation.objects.get(pk=rent_pk)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReservationSerializer(reservation)
        return Response(serializer.data)
    
    
@api_view(['DELETE'])
def cancel_reservation(request, rent_pk):
    """
    API endpoint for cancelling a specific Booking.
    """
    try:
        reservation = Reservation.objects.get(pk=rent_pk)
    except Reservation.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        reservation.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
def book_car(request):
    """
    API endpoint for booking an available car.
    """
    if request.method == 'POST':
        serializer = ReservationSerializer(data=request.data)
            
        if serializer.is_valid():
            current_date = date.today()
            issue_date = serializer.validated_data['issue_date']
            return_date = serializer.validated_data['return_date']

            car = serializer.validated_data['car']
            reservations = Reservation.objects.all().filter(car=car.id)

            # Check if the issue_date of new reservation doesn't clash with any previous reservations
            for r in reservations:
                if r.issue_date <= issue_date <= r.return_date:
                    content = {"message":"The selected car is not available on this date"}
                    return Response(data=json.dumps(content), status=status.HTTP_400_BAD_REQUEST)

            # Check whether issue_date is not older than today's date, and is less equal to return_date
            if current_date <= issue_date and issue_date <= return_date:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    
    




