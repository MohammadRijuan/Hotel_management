from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=40, unique=True, blank=True)

    def __str__(self):
        return self.name
    

class Hotel(models.Model):
    categories = models.ManyToManyField(Category)
    title = models.CharField(max_length=120)
    description = models.TextField()
    image = models.ImageField(upload_to='hotel/media/uploads',blank=True,null=True)
    phone_no = models.CharField(max_length=50,blank=True,null=True)
    price = price = models.DecimalField(max_digits=12, decimal_places=2)
    rooms = models.PositiveIntegerField(default = 0)


    def __str__(self):
        return self.title
    
from django.contrib.auth.models import User

class Review(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.CharField(max_length=5,choices=[
    ('⭐', '⭐'),
    ('⭐⭐', '⭐⭐'),
    ('⭐⭐⭐', '⭐⭐⭐'),
    ('⭐⭐⭐⭐', '⭐⭐⭐⭐'),
    ('⭐⭐⭐⭐⭐', '⭐⭐⭐⭐⭐'),
])
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class BookingHotelHistory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel,on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    rooms = models.PositiveIntegerField(default = 1)


from django.db import models

class Contact_Us(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.name} ({self.email})"
