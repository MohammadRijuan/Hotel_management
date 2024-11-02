from django.shortcuts import render,redirect
from django.views.generic import FormView
# Create your views here.
from . forms import RegForm
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages


class UserRegistrationView(FormView):
    template_name ='user_registration.html'
    form_class = RegForm
    success_url = reverse_lazy('login')

    def form_valid(self,form):
        user = form.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        confirm_link=f"https://hotel-management-v7no.onrender.com/accounts/active/{uid}/{token}"
        email_subject = "Confirm Your Email"
        email_body = render_to_string('confirm_email.html',{'confirm_link': confirm_link})

        email = EmailMultiAlternatives(email_subject, '' , to=[user.email])
        email.attach_alternative(email_body,"text/html")
        email.send()
        messages.success(self.request,"Check your email for confirmation.")
        return redirect("login")
    
    def form_invalid(self, form):
        error_data = form.errors.as_data()
        if error_data:
            error_message = error_data.popitem()[1][0].message
            messages.error(self.request, error_message)
        return super().form_invalid(form)


from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    


from django.contrib.auth.views import LoginView

class UserLoginView(LoginView):
    template_name='user_login.html'
    
    def get_success_url(self):
        return reverse_lazy ('profile')
    

from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout

class UserLogoutView(LogoutView):
    def get_success_url(self):

        if self.request.user.is_authenticated:
            logout(self.request)
            messages.success(self.request,'logged out successfully')

        return reverse_lazy('home')



from django.views import View
from . forms import UserUpdateForm
from django.shortcuts import redirect

class UserAccountUpdateView(View):
    template_name = 'profile.html'
    
    def get(self, request):
        # Ensure related instances exist before initializing the form
        
        user = request.user
        UserAccount.objects.get_or_create(user=user)
        UserAddress.objects.get_or_create(user=user)

        form = UserUpdateForm(instance=user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # Ensure related instances exist before initializing the form
        
        user = request.user
        UserAccount.objects.get_or_create(user=user)
        UserAddress.objects.get_or_create(user=user)

        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})
    

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView

class ChangePassView(PasswordChangeView):
    template_name = 'password_change.html'
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'You have changed your password successfully')
        return super().form_valid(form)
