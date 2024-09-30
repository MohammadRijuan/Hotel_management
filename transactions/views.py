from django.shortcuts import render

# Create your views here.
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from . models import Transaction
from django.urls import reverse_lazy

class TransactionCreateMixin(LoginRequiredMixin,CreateView):
    template_name = 'transaction_form.html'
    model = Transaction
    success_url = reverse_lazy('transaction_report')
    title = ''

    def get_form_kwargs(self): #ata amdr data pass korbe amdr form ke
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account' : self.request.user.account,
        })
        return kwargs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'title' : self.title
        })
        return context
    

from . forms import DepositForm
from django.contrib import messages
from .constants import DEPOSIT

class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Deposit'

    def get_initial(self):
        initial = {'transaction_type':DEPOSIT}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        account.balance += amount 
        account.save(
            update_fields=[
                'balance'
            ]
        )

        messages.success(
            self.request,
            f'{"{:,.2f}".format(float(amount))}$ was deposited to your account successfully'
        )

        # send_transaction_email(self.request.user,amount,"Deposite Message","transactions/deposit_email.html")
        return super().form_valid(form)
    

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from datetime import datetime
from django.db.models import Sum

class TransactionReportView(LoginRequiredMixin,ListView):
    template_name = 'transaction_report.html'
    model = Transaction
    balance = 0

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account = self.request.user.account
        )

        #string akare nilam
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')

        if start_date_str and end_date_str:
            #date e convert korlam
            start_date  = datetime.strptime(start_date_str,"%Y-%M-%d").date()
            end_date  = datetime.strptime(start_date_str,"%Y-%M-%d").date()
            
            queryset = queryset.filter(timestamp__date__gte = start_date, timestamp__date__lte =end_date)
            
            
            self.balance = Transaction.objects.filter(timestamp__date__gte = start_date , timestamp__date__lte = end_date).aggregate(Sum('amount'))
            ['amount_sum']

        else:
            self.balance = self.request.user.account.balance

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account':self.request.user.account

        })
        return context

    
    


