from django.urls import path
from .views import showing_booking_history,cancel_hotel,Hotel_list_category,Hotel_list,DetailHotelView,booking_hotels,Contact_US_view


urlpatterns = [
    
    path('hotels/<slug:slug>/hotel/', booking_hotels, name='book_hotel'),
    path('hotels/<int:hotel_id>/', booking_hotels, name='book_hotel'),

    path('category/<slug:category_slug>/', Hotel_list_category, name='Hotel_list_category'),

    path('booking-history/', showing_booking_history, name='booking_history'),
    path('booking-history/<int:booking_id>/cancel/', cancel_hotel, name='cancel_hotel'),

    path('hotel_list/', Hotel_list, name='hotel_list'),
    path('hotels/details/<int:pk>/', DetailHotelView.as_view(), name='hotel_detail'),

    path('contact/', Contact_US_view, name='contact'),


     
]