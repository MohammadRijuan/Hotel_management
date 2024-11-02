from django import forms
from django.contrib.auth.models import User
from . models import UserAccount,UserAddress
from django.contrib.auth.forms import UserCreationForm


class RegForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=[
    ('Male','Male'),
    ('Female','Female'),
    ])
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.IntegerField()
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username','password1','password2','first_name','last_name','email','birth_date','gender','postal_code','city','country']
    
    def save(self,commit=True):
        curr_user = super().save(commit=False) 

        if commit == True:
            curr_user.save()
            
            gender = self.cleaned_data.get('gender')
            postal_code = self.cleaned_data.get('postal_code')
            country = self.cleaned_data.get('country')
            birth_date = self.cleaned_data.get('birth_date')
            city = self.cleaned_data.get('city')
            street_address = self.cleaned_data.get('street_address')
    

            UserAddress.objects.create(
                user= curr_user,
                postal_code =postal_code,
                country = country,
                city=city,
                street_address =street_address,
            )

            UserAccount.objects.create(
                user = curr_user,
                gender =gender,
                birth_date =birth_date,
                account_no = 100000 + curr_user.id
            )
        
        return curr_user


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })



class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
    ])
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20)  # Changed to CharField to allow flexibility
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'gender', 'birth_date', 
                  'street_address', 'city', 'postal_code', 'country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })

        # Pre-populate fields with existing user account data
        if self.instance:
            user_account = getattr(self.instance, 'account', None)
            user_address = getattr(self.instance, 'address', None)

            if user_account:
                self.fields['gender'].initial = user_account.gender
                self.fields['birth_date'].initial = user_account.birth_date

            if user_address:
                self.fields['street_address'].initial = user_address.street_address
                self.fields['city'].initial = user_address.city
                self.fields['postal_code'].initial = user_address.postal_code
                self.fields['country'].initial = user_address.country

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

            # Update or create the UserAccount
            user_account, created = UserAccount.objects.get_or_create(user=user)
            user_account.gender = self.cleaned_data['gender']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()

            # Update or create the UserAddress
            user_address, created = UserAddress.objects.get_or_create(user=user)
            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.country = self.cleaned_data['country']
            user_address.save()
            print(user_address)

        return user
