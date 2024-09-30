from django.shortcuts import redirect, render,get_object_or_404

# Create your views here.
from . models import Hotel,BookingHotelHistory,Category

def Hotel_list_category(request,category_slug = None):
    hotels = Hotel.objects.all()
    category = None

    if category_slug is not None:
        category = get_object_or_404(Category,slug = category_slug)
        hotels = hotels.filter(categories = category)
    
    categories = Category.objects.all()
    return render(request,'index.html',{'hotels':hotels , 'categories':categories , 'category':category})




from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# for email
def booking_hotel_email(user,title,subject,price,template):
    message = render_to_string(template,{
        'user':user,
        'title':title,
        'price':price
    })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

from accounts.models import UserAccount
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def booking_hotels(request,hotel_id):
    hotel = get_object_or_404(Hotel,pk=hotel_id)
    account = UserAccount.objects.get(user=request.user)

    if hotel.rooms < 1:
        messages.error(request,'Sorry, Your Desired hotel room is not available')
        return redirect('home')
    
    if hotel.price > account.balance:
        messages.error(request,'Insufficient Balance!')
        return redirect('booking_history')
    
    hotel.rooms -= 1
    hotel.save()
    account.balance -= hotel.price
    account.save(update_fields=['balance'])
    booking, created = BookingHotelHistory.objects.get_or_create(user=request.user, hotel=hotel)
    if not created:
        booking.rooms +=1
        booking.save()

    booking_hotel_email(request.user,hotel.title,"Hotel Booked Successfully",hotel.price,"booking_email.html")
    messages.success(request,f'You have booked an hotel room successfully {hotel.title}')
    
    return redirect('booking_history')


@login_required
def cancel_hotel(request,booking_id):
    booking = get_object_or_404(BookingHotelHistory,pk=booking_id)
    user_account = UserAccount.objects.get(user=request.user)

    user_account.balance += booking.hotel.price # cancel korle joto tuku jani hotel teke tk back dewa hoina
    user_account.save()

    booking.hotel.rooms +=1
    booking.hotel.save()
    booking.rooms -= 1

    if booking.rooms < 1:
        booking.delete()
        messages.warning(request,'You have cancelled the booking...Sorry! You Wont get the money back')
    
    else:
        booking.save()
        messages.success(request,'You have cancelled the booking...Sorry! You Wont get the money back')
    # email option
    return redirect('booking_history')


def showing_booking_history(request):
    bookings = BookingHotelHistory.objects.filter(user = request.user).order_by('-booking_date')

    for booking in bookings:
        booking.total_price_cur = booking.hotel.price * booking.rooms
    total_price = sum(booking.hotel.price * booking.rooms for booking in bookings)
    return render(request,'booking_history.html',{'bookings':bookings ,'total_price':total_price})


from django.views.generic import DetailView
from . forms import ReviewForm
from .models import Review,Category,Hotel

class DetailHotelView(DetailView):
    model = Hotel
    template_name = 'hotel_detail.html'
    form_class = ReviewForm
 
    def post(self, request, *args, **kwargs):
        hotel = self.get_object()
        comment_form = self.form_class(data=request.POST)
        
        
        user_has_booked = BookingHotelHistory.objects.filter(user=request.user, hotel=hotel).exists()
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.hotel = hotel
            new_comment.user = request.user  # request.user user instance hisebe teke jabe
            new_comment.save()
             
        return self.get(request, *args, **kwargs)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hotel = self.object
        reviews = Review.objects.filter(hotel=hotel)
        # reviews=Hotel.reviews.all()
        comment_form = self.form_class()
        
        if self.request.user.is_authenticated:
            user_has_booked = BookingHotelHistory.objects.filter(user=self.request.user, hotel=hotel).exists()
        else:
            user_has_booked = False

        context['reviews'] = reviews
        context['comment_form'] = comment_form
        context['user_has_booked'] = user_has_booked 
        return context



def Hotel_list(request, category_slug=None):
    hotels = Hotel.objects.all()

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        hotels = hotels.filter(categories=category)

    categories = Category.objects.all()
    return render(request,'hotel_list.html', {'hotels':hotels, 'categories':categories})



from .forms import ContactUsForm

def Contact_US_view(request):
    if request.method == 'POST':
        contacts = ContactUsForm(request.POST)
        if contacts.is_valid():
            contacts.save() 
            messages.success(request, "Your message has been sent successfully!")
            return redirect('home') 
    else:
        contacts = ContactUsForm()
    
    return render(request, 'contact_us.html', {'contacts': contacts})
