from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.db import transaction, DatabaseError
from django.shortcuts import *
from django import forms
from func.models import *
from django import http
from django.http import HttpResponseRedirect, HttpResponse
import hashlib
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import HttpResponse
from django.core import serializers
from django.contrib.auth.models import User, Group
import json
from django.utils import timezone
import datetime
import json
import math
import re
from django.contrib.auth.hashers import make_password, check_password

from django.views.decorators.csrf import csrf_exempt


class UserForm(forms.Form):
    username = forms.CharField(label='user', max_length=10)
    password = forms.CharField(label='passwd', widget=forms.PasswordInput())

# class RegisterIndiForm(forms.Form):
#     email = forms.CharField(label='email', max_length=100)
#     password1 = forms.PasswordInput
#     password2 = forms.PasswordInput
#     firstName = forms.CharField(label='inputFirstName', max_length=30)
#     lastName = forms.CharField(label='inputLastName', max_length=30)
#     phoneNo = forms.CharField(label='inputPhoneNo', max_length=10)
#     streetAddr = forms.CharField(label='inputStreetAddr', max_length=50)
#     city = forms.CharField(label='inputCity', max_length=30)
#     state = forms.CharField(label='inputState', max_length=2)
#     zipcode = forms.CharField(label='inputZipcode', max_length=5)
#     customerType = forms.CharField(label='inputCustomerTyep', max_length=1)
#     DLNO = forms.CharField(label='inputDriverLicenceNo', max_length=10)
#     insuranceCompany = forms.CharField(label='inputInsuranceCompany', max_length=30)
#     insPolicyNo = forms.CharField(label='inputInsurancePolicyNo', max_length=30)

def validateEmail( email ):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email( email )
        return True
    except ValidationError:
        return False


# def test(request):
#     return render(request, 'test.html');
#
#
# def indexView(request):
#     if request.method == 'GET':
#         v_list = Vehicle.objects.all()
#     return render(request, 'index.html', json.dumps([v_list]))


# def login_view(request):
#     if request.method == 'GET':
#         return render(request, 'login.html')
#    # request.session.delete()
#     u_email = request.session.get('u_email', None)
#     if u_email is not None:
#         return HttpResponseRedirect('/profile/')
#     else:
#         if u_email is not None:
#             return render(request, 'logouttest.html', {'w':u_email})
#         if request.method == 'POST':
#             email = request.POST.get('email')
#             password = request.POST.get('password')
#             testUser = authenticate(username=email, password=password)
#             if testUser is None:
#                 return HttpResponse("User not exist!")
#             # 把表单中取到的值和数据库里做对比
#             else:
#                     #login(request, user)
#                 message:'"Success!"'
#                 request.session['u_email'] = email
#                 # request.session['u_firstName'] = user[0].firstName
#                 # request.session['u_lastName'] = user[0].lastName
#                 # request.session['u_password'] = user[0].password
#                 # request.session['phoneNo'] = user[0].phoneNo
#                 # request.session['streetAddr'] = user[0].streetAddr
#                 # request.session['city'] = user[0].city
#                 # request.session['state'] = user[0].state
#                 # request.session['zipcode'] = user[0].zipcode
#                 login(request, testUser)
#                 user = Customer.objects.filter(emailID=email)
#
#                 # midUser = user[0]
#                 # user1 = serializers.serialize("json", [midUser])
#                 # request.session['user'] = user1
#                 return render(request, 'test.html', {'emailID':email})
#                 #return HttpResponseRedirect(r'^test/')

# def profile(request):
#     uEmail = request.session.get('u_email', None)
#     if uEmail is None:
#         return render(request, 'login.html')
#     else:
#         userTest = Customer.objects.filter(emailID = uEmail)
#         result = [userTest[0].emailID, userTest[0].firstName]
#     return render(request, 'profile.html', {'List': result})

# def logout_view(request):
#     logout(request)
#     request.session.delete('u_email')
#     request.session.clear()
#     return render(request, 'login.html', {'dispErr': 'none'})

def index(request):
    pass
    return render(request, 'index.html')


def registerIndi(request, **kwargs):
    if not request.POST:
        return render(request, 'register.html')
    email = request.POST.get('inputEmail')
    password1 = request.POST.get('inputPassword')
    password2 = request.POST.get('re_inputPassword')
    firstName = request.POST.get('inputFirstName')
    lastName = request.POST.get('inputLastName')
    phoneNo = request.POST.get('inputPhoneNo')
    streetAddr = request.POST.get('inputStreetAddr')
    city = request.POST.get('inputCity')
    state = request.POST.get('inputState')
    zipcode = request.POST.get('inputZipcode')
    DLNO = request.POST.get('inputDriverLicenceNo')
    insuranceCompany = request.POST.get('inputInsuranceCompany')
    insPolicyNo = request.POST.get('inputInsurancePolicyNo')
    if email and password1 and password2 and firstName and lastName and phoneNo and streetAddr and city and state and zipcode and DLNO and insuranceCompany and insPolicyNo:
        if not validateEmail(email):
            messages.error(request, 'Please input the valid email address!!')
            return redirect("/register")
        exist = User.objects.filter(username=email)
        if exist:
            messages.error(request, 'This email has been used!')
            return redirect("/register")
        if password1 != password2:
            messages.error(request, 'Password is not match!')
            return redirect("/register")

        cust = Customer(emailID=email, firstName=firstName, lastName=lastName, phoneNo=phoneNo, streetAddr=streetAddr,
                        city=city, state=state, zipcode=zipcode, customerType='I')
        indiU = individualCustomer(customerID=cust, driverLicenceNo=DLNO, insuranceCompany=insuranceCompany, insurancePolicyNo=insPolicyNo)
        try:
            with transaction.atomic():
                cust.save()
                indiU.save()
                messages.error(request, 'Success!')
                user = User.objects.create_user(username=email, password=password1, is_staff=True)
                user.groups.add(3)
                logout(request)
                login(request, user)
            return redirect("/admin")
        except DatabaseError:
            messages.error(request, 'Failed! Please check your information!')
            return redirect("/register")
    else:
        messages.error(request, 'Please fulfill the information!')
        return redirect("/register")

def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def registerCorp(request, **kwargs):
    if not request.POST:
        return render(request, 'register.html')
    email = request.POST.get('inputEmail')
    password1 = request.POST.get('inputPassword')
    password2 = request.POST.get('re_inputPassword')
    firstName = request.POST.get('inputFirstName')
    lastName = request.POST.get('inputLastName')
    phoneNo = request.POST.get('inputPhoneNo')
    streetAddr = request.POST.get('inputStreetAddr')
    city = request.POST.get('inputCity')
    state = request.POST.get('inputState')
    zipcode = request.POST.get('inputZipcode')
    employeeID = request.POST.get('inputEmployeeID')
    corporationID = request.POST.get('inputCorporationID')
    if email and password1 and password2 and firstName and lastName and phoneNo and streetAddr and city and state and zipcode and employeeID and corporationID:
        if not validateEmail(email):
            messages.error(request, 'Please input the valid email address!!')
            return redirect("/register")
        exist = Customer.objects.filter(emailID=email)
        if exist:
            messages.error(request, 'This email has been used!')
            return redirect("/register")

        if password1 != password2:
            messages.error(request, 'Password is not match!')
            return redirect("/register")
        corp = Corporation.objects.filter(registrationNo=corporationID).first()
        if not corp:
            messages.error(request, 'Corporation not exists!')
            return redirect("/register")

        cust = Customer(emailID=email, firstName=firstName, lastName=lastName, phoneNo=phoneNo, streetAddr=streetAddr, city=city, state=state, zipcode=zipcode, customerType = 'C')
        #user = User(username=email, password=password1, is_staff=True)
        corpU = corporationCustomer(customerID=cust, employeeID=employeeID, corporationID = corp)
        try:
            with transaction.atomic():
                cust.save()
                #user.save()
                corpU.save()
                #login(request, user)
                #raise DatabaseError
                messages.error( request, 'Success!')
            user = User.objects.create_user(username=email, password=password1, is_staff=True)
            # my_group = Group.objects.get(name='Corporation_User')
            # my_group.user_set.add(user)
            user.groups.add(2)
            logout(request)
            login(request, user)
            return redirect("/admin")
        except DatabaseError:
            messages.error(request, 'Failed! Please check your information!')
            return redirect("/register")
        #cust=Customer.objects.create(emailID=email, firstName=firstName, lastName=lastName, phoneNo=phoneNo, streetAddr=streetAddr, city=city, state=state, zipcode=zipcode, customerType = 'C')
        #mid = Customer.objects.filter(emailID=email)
        #midID = mid.values('customerID')
        # user = User.objects.create_user(username=email, password=password1)
        # login(request, user)
        # corporationCustomer.objects.create(customerID=cust, employeeID=employeeID, corporationID = corp.corporationID)
        # response = http.JsonResponse({"code": 0, "errmsg": "Success!"})
        # response.set_cookie("username", user.username, max_age=3600 * 24 * 14)
        # return render(request,'index.html')
    else:
        messages.error(request, 'Please fulfill the information!')
        return redirect("/register")

def register(request, **kwargs):
    if not request.POST:
        return render(request, 'register.html')
    individual = request.POST.get('Individual')
    if individual:
        return redirect("/registerIndi")
    else:
        return redirect("/registerCorp")

# def makeOrder(request):
#     if request.GET:
#         return render(request, 'order.html')
#     if request.POST:
#         pickupDate = request.POST.get('pickupDate')
#         vehicleID = request.POST.get('vehicleID')
#         pickupOffice = request.POST.get('pickupOffice')
#         customerID = request.POST.get('customerID')
#         couponID = request.POST.get('couponID')
#         coupon = Coupon.objects.filter(couponID = couponID)
#         customer = Customer.objects.filter(customerID = customerID)
#         if Coupon_Customer.objects.filter(customerID = customerID) is not None:
#             return HttpResponse('Coupon has been used!')
#         else:
#             Coupon_Customer.objects.create(customerID=customer, couponID=coupon)
#             pendingService.objects.

