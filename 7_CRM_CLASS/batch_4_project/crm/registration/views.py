from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse

from .models import*

from django.core.mail import send_mail
import secrets

from rest_framework import viewsets
from .serializers import RegistrationSerializer

# Create your views here.

def register(req):
    if req.method =='GET':

        return render(req,'signup.html')
    else:
        fname = req.POST.get("fname")
        email = req.POST.get("email")
        date_of_birth = req.POST.get("date_of_birth")
        password = req.POST.get("password")
        con_pw = req.POST.get("con_pw")

        if(fname=='' or email=='' or password =='' or con_pw==''):
            return HttpResponse("the field can not be empty")
        elif (password!=con_pw):
            return HttpResponse("The Password Does not match")
        else:
            reg_obj =Registration()

            reg_obj.name = fname 
            reg_obj.email = email
            reg_obj.password = password
            reg_obj.date_of_birth = date_of_birth

            if(Registration.objects.filter(email=email).exists()):
                return HttpResponse("the email is already existed")
            else:

                reg_obj.save()
        return redirect("customer")

def edit_customer(req,cid):
    # return HttpResponse("je")
    #select * from table where id = cid
    get_cust_data = get_object_or_404(Registration, id=cid)
    if req.method == "GET":
        data = {'get_data':get_cust_data}
        return render(req,'customer_edit.html',data)
    else:
        fname = req.POST.get("fname")
        email = req.POST.get("email")
        date_of_birth = req.POST.get("date_of_birth")
        password = req.POST.get("password")
        con_pw = req.POST.get("con_pw")



        if(fname=='' or email=='' or password =='' or con_pw==''):
            return HttpResponse("the field can not be empty")
        elif (password!=con_pw):
            return HttpResponse("The Password Does not match")
        else:
            # return HttpResponse("hello")
            get_cust_data.name = fname
            get_cust_data.email = email 
            get_cust_data.password = password
            get_cust_data.date_of_birth = req.POST.get("date_of_birth")
            get_cust_data.save()
            return redirect('customer')
        


def show_customer_bill(req):
    if req.method =='GET':

        all_customers = Registration.objects.all() #select * from registration table
        all_bill = Bill.objects.select_related('customer_id').all
        all_data = {'customers':all_customers,'bill':all_bill}
        return render(req,'bill.html',all_data)
    else:
        customer_id = req.POST.get('customer')
        customer_id_obj = Registration.objects.get(id=customer_id) #select customer_id from registration where id = customer_id 
        bill_id = req.POST.get('bill_id')
        bill_amount = req.POST.get('bill_amount')
        bill_picture = req.FILES.get('bill_picture')

        bill_obj = Bill()
        otp = str(secrets.randbelow(9000) + 1000)
        
        send_mail(
            'Your OTP Code',
            f'Your OTP code is: {otp}',
            'innovativeskillsbd@gmail.com', #email host
            ['tahsinabdullah107@gmail.com'],
            fail_silently=False,
        )

        bill_obj.customer_id = customer_id_obj
        bill_obj.bill_id = bill_id
        bill_obj.bill_amount = bill_amount
        bill_obj.bill_code = otp 
        bill_obj.bill_status = "no"

        bill_obj.bill_picture = bill_picture
        bill_obj.save()
        return redirect('customer_bill')
def delete_customer(req,cid):
    get_cust_data = get_object_or_404(Registration,id=cid)
    get_cust_data.delete()
    return redirect('customer')
def show_customer(req):

    data = Registration.objects.all() #select * from registraion

    all_data = {"all_data1":data}
    return render(req,'customer.html',all_data)


def login(req):
    if req.method == "GET":

        return render(req,'login.html')

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer


