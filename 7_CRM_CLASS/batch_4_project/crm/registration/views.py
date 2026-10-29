from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse

from .models import*

from django.core.mail import send_mail
from django.core.cache import cache
import secrets

from rest_framework import viewsets # controls CRUD(Create, Read, Update, Delete) actions
# from .serializers import RegistrationSerializer
from .serializers import RegistrationSerializer, LoginSerializer

from rest_framework.views import APIView # recives API request
from rest_framework.response import Response # returns JSON
from rest_framework.permissions import AllowAny, IsAuthenticated # allows login without already having a token
from rest_framework.permissions import IsAuthenticated # requires a valid access token.

from rest_framework.filters import SearchFilter # allows filtering of API results
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from django.utils.dateparse import parse_date
from rest_framework.exceptions import ValidationError





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
                # Customer data changed, so remove the old customer-list copy.
                cache.delete('customer_list')
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
            # Customer data changed, so remove the old customer-list copy.
            cache.delete('customer_list')
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
    # Customer data changed, so remove the old customer-list copy.
    cache.delete('customer_list')
    return redirect('customer')

def show_customer(req):
    # The key is the label used to find this one cached value.
    cache_key = 'customer_list'
    data = cache.get(cache_key)

    if data is None:
        # Cache miss: PostgreSQL is asked only when cache has no value.
        # values() keeps the classroom cache free of the plain-text password field.
        data = list(Registration.objects.values('id', 'name', 'email', 'date_of_birth'))
        cache.set(cache_key, data, timeout=60)
        cache_status = 'Database used: cache miss (saved for 60 seconds)'
    else:
        # Cache hit: use the fast temporary copy from Django memory.
        cache_status = 'Fast memory used: cache hit'

    all_data = {"all_data1":data, "cache_status": cache_status}
    return render(req,'customer.html',all_data)


def login(req):
    if req.method == "GET":

        return render(req,'login.html')



class LoginAPIView(APIView):
    permission_classes = [AllowAny]
#     APIView creates an API controller.
#     AllowAny lets users attempt login without already having a token.

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Send the incoming email and password from request.data 
        # to LoginSerializer. and then validates with is_valid()


        return Response(serializer.validated_data)
# POST data
# → LoginSerializer
# → validate email/password
# → return access + refresh tokens



class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # This API is protected. 
    # Only a request containing a valid access token can enter.

    def get(self, request):
        return Response({
            'id': request.user.id,
            'username': request.user.username,
            'email': request.user.email,
        })
# Valid access token
# → Django identifies the user
# → request.user contains that user
# → API returns basic profile data


class RegistrationPagination(PageNumberPagination):
    # Show 10 records per page; allow a request for up to 50.
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = RegistrationPagination
    # queryset → provides Registration records
    # serializer_class → converts or validates those records/data
    # ModelViewSet → connects and controls both automatically
    # IsAuthenticated -> Registration list, create, update, and delete now require a valid JWT access token.


    # Let the registration list be searched by name or email.
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'email']

    # Use ID order by default; allow clients to choose these fields.
    ordering = ['id']
    ordering_fields = ['id', 'name', 'email', 'date_of_birth']



    def get_queryset(self):
        queryset = super().get_queryset()

        # Match the whole email address, ignoring letter case.
        email = self.request.query_params.get('email')
        if email:
            queryset = queryset.filter(email__iexact=email)

        # Read the optional date range from the URL.
        from_text = self.request.query_params.get('dob_from')
        to_text = self.request.query_params.get('dob_to')

        try:
            from_date = parse_date(from_text) if from_text else None
            to_date = parse_date(to_text) if to_text else None
        except ValueError:
            raise ValidationError({'date': 'Use YYYY-MM-DD for dob_from and dob_to.'})

        if (from_text and from_date is None) or (to_text and to_date is None):
            raise ValidationError({'date': 'Use YYYY-MM-DD for dob_from and dob_to.'})

        if from_date and to_date and from_date > to_date:
            raise ValidationError({'date': 'dob_from must be before or equal to dob_to.'})

        if from_date:
            queryset = queryset.filter(date_of_birth__gte=from_date)
        if to_date:
            queryset = queryset.filter(date_of_birth__lte=to_date)

        return queryset


