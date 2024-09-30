from django.shortcuts import render, get_object_or_404,redirect
from django.views.generic import DetailView
from hotel.models import Hotel, Review,Category
from hotel.forms import ReviewForm
from hotel.forms import ContactUsForm
from django.contrib import messages


# Create your views here.
def HomeView(request,category_slug=None):
    # showing hotel list
    hotels = Hotel.objects.all()

    if category_slug is not None:
        category = get_object_or_404(Category, slug=category_slug)
        hotels = hotels.filter(categories=category)

    categories = Category.objects.all()


    # showing contact list
    if request.method == 'POST':
        contacts = ContactUsForm(request.POST)
        if contacts.is_valid():
            contacts.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('home')
    else:
        contacts = ContactUsForm()

    return render(request, 'index.html', {'hotels': hotels,'categories': categories,'contacts': contacts})





