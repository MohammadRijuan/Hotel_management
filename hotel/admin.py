from django.contrib import admin
from . models import Hotel,Category,Review,BookingHotelHistory,Contact_Us
# Register your models here.

admin.site.register(Hotel)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category,CategoryAdmin)

admin.site.register(Review)
admin.site.register(BookingHotelHistory)
admin.site.register(Contact_Us)
