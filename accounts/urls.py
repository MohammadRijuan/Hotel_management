from django.urls import path,include
from . views import UserRegistrationView,activate,UserLoginView,ChangePassView,UserAccountUpdateView,UserLogoutView

urlpatterns = [
    
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('active/<uid64>/<token>/', activate, name ='activate'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('logout/',UserLogoutView.as_view(),name='logout'),
    path('profile/',UserAccountUpdateView.as_view(),name='profile'),
    path('password_change/',ChangePassView.as_view(), name='password' )
]