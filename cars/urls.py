from django.urls import path
from . import views


urlpatterns = [
    path("home",views.home),
    path("customers",views.view_all_customer),
    path("customers/<int:cust_pk>/",views.customer_details),
    path("customers/add/",views.add_customer),
    path("customers/<int:cust_pk>/update",views.update_customer_details),
    path("customers/<int:cust_pk>/delete",views.delete_customer),
    
    path("cars",views.view_all_cars),
    path("cars/<int:car_pk>/",views.car_details),
    path("cars/add/",views.add_car),
    path("cars/<int:car_pk>/update",views.update_car_details),
    path("cars/<int:car_pk>/delete",views.delete_car),
    
    path('rent/', views.view_all_reservations),
    path('rent/book/', views.book_car), # API 2: Book an available car
    path('rent/<int:rent_pk>/', views.view_reservation_details),
    path('rent/<int:rent_pk>/cancel/', views.cancel_reservation)
]