from django import forms
from . models import Review,Hotel


class HotelForm(forms.ModelForm):
    class Meta:
        model = Hotel
        fields = ['title', 'description', 'image', 'phone_no','price','categories']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment','rating']

from . models import Contact_Us

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = Contact_Us
        fields = ['name', 'email', 'message']