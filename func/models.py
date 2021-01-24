from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.html import format_html

from django.db.models.signals import *
from django.dispatch import receiver


class Corporation(models.Model):
    corporationID = models.AutoField(db_column='CORPORATION_ID', verbose_name='Corporation',primary_key=True)
    corpName = models.CharField(db_column='CORPORATION_NAME', max_length=30)
    registrationNo = models.CharField(db_column='REGISTRATION_NO', max_length=5)
    def __str__(self):
        return str(self.corpName)

class Customer(models.Model):
    INDIVIDUAL = 'I'
    CORPORATION = 'C'
    CUSTOMERTYPE = [
        (INDIVIDUAL, 'I'),
        (CORPORATION, 'C')
    ]

    customerID = models.AutoField(db_column='USER_ID', verbose_name='Customer ID', primary_key=True)  # Field name made lowercase.
    firstName = models.CharField(db_column='FIRST_NAME', max_length=30)  # Field name made lowercase.
    lastName = models.CharField(db_column='LAST_NAME', max_length=30)
    # accountName = models.CharField(db_column='ACCOUNT_NAME', max_length=30)
    # password = models.CharField(db_column='PASSWORD', max_length=16)  # Field name made lowercase.
    emailID = models.CharField(db_column='EMAIL_ID', verbose_name='Email',max_length=100, unique=True)
    phoneNo = models.CharField(db_column='PHONE_ID', verbose_name='Phone Number',max_length=10)
    streetAddr = models.CharField(db_column='STREET_ADDR', verbose_name='Street Address',max_length=50)
    city = models.CharField(db_column='CITY', verbose_name='City',max_length=30)
    state = models.CharField(db_column='STATE',verbose_name='Zipcode', max_length=2)
    zipcode = models.CharField(db_column='ZIPCODE', max_length=5)
    customerType = models.CharField(db_column='CUST_TYPE', max_length=1, choices=CUSTOMERTYPE)

    def __str__(self):
        return str(self.emailID)
    class Meta:
        unique_together = ['emailID', 'phoneNo']


class Coupon(models.Model):
    couponID = models.CharField(db_column='COUPON_ID', verbose_name='Coupon Code', primary_key=True, max_length=10)
    discount = models.DecimalField(db_column='DISCOUNT', max_digits=2, decimal_places=2)
    validFrom = models.DateField(db_column='VALID_FROM', null=True, blank=True)
    validTo = models.DateField(db_column='VALID_TO', null=True, blank=True)
    is_corp = models.BooleanField(db_column='IS_COUPON', default=False)
    corporation = models.ForeignKey('Corporation', on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        corporation = 'None'
        if self.corporation is not None:
            corporation = self.corporation
        vFrom = '--'
        vTo = '--'
        if self.validFrom is not None:
            vFrom = self.validFrom
        if self.validTo is not None:
            vTo = self.validTo
        return str(str(self.couponID) + ' , DISCOUNT RATE' + str(self.discount) + ' , validDate: ' + str(vFrom) + '~' + str(vTo) + ' Corporation: ' + str(corporation))
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(validFrom__lt=models.F('validTo')), name='from_date_lt_to')
        ]


class Coupon_Customer(models.Model):
     couponID = models.ForeignKey('Coupon', on_delete=models.CASCADE)
     customerID = models.ForeignKey('Customer', on_delete=models.CASCADE)
     def __str__(self):
        return str(str(self.couponID) + ' -- ' + str(self.customerID))


class individualCustomer(models.Model):
    customerID = models.ForeignKey('Customer', verbose_name='Email',primary_key=True, on_delete=models.CASCADE)
    driverLicenceNo = models.CharField(db_column='DRIVER_LICENCE_NO', verbose_name='Driver Licence No.',max_length=10)
    insuranceCompany = models.CharField(db_column='INSURANCE_COMPANY', verbose_name='Insurance Company',max_length=30)
    insurancePolicyNo = models.CharField(db_column='INSURANCE_POLICY_NO', verbose_name='Insurance Policy No.',max_length=30)
    def __str__(self):
        return str(self.customerID)

class corporationCustomer(models.Model):
    customerID = models.ForeignKey('Customer', primary_key=True, verbose_name='Email',on_delete=models.CASCADE)
    employeeID = models.CharField(db_column='EMPLOYEE_ID', verbose_name='Employee ID',max_length=10)
    corporationID = models.ForeignKey('Corporation', verbose_name='Corporation',on_delete=models.CASCADE)
    def __str__(self):
        return str(self.customerID)

class vehicleClass(models.Model):
    typeID = models.AutoField(db_column='TYPE_ID', primary_key=True)
    type = models.CharField(db_column='TYPE', max_length=20)
    rentCharge = models.DecimalField(db_column='R_RATE', max_digits=5, decimal_places=2)
    extraCharge = models.DecimalField(db_column='EXTRA_FEE', max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.type)


class Office(models.Model):
    ofcID = models.AutoField(db_column='OFFICE_ID', verbose_name='OfficeID',primary_key=True)
    ofcStreetAddr = models.CharField(db_column='STREET_ADDR', verbose_name='Office Location',max_length=50)
    ofcCity = models.CharField(db_column='CITY', verbose_name='City',max_length=30)
    ofcState = models.CharField(db_column='STATE', verbose_name='State',max_length=2)
    ofcZipcode = models.CharField(db_column='ZIPCODE', verbose_name='Zipcode',max_length=5)
    ofcPhoneNo = models.CharField(db_column='PHONE_NO', verbose_name='Contact Number',max_length=10)

    def __str__(self):
        return str(self.ofcStreetAddr + ' , ' + self.ofcCity + ' , ' + self.ofcState)

class Vehicle(models.Model):
    vehicleID = models.AutoField(db_column='VEHICLE_ID', primary_key=True)
    make = models.CharField(db_column='MAKE', max_length=20)
    model = models.CharField(db_column='MODEL', max_length=20)
    year = models.CharField(db_column='YEAR', max_length=4)
    vin = models.CharField(db_column='VIN', verbose_name='Vehicle Identification Number', max_length=7)
    licensePlateNo = models.CharField(db_column='LICENSE_PLATE_NO', verbose_name='License Plate Number', max_length=6)
    typeID = models.ForeignKey('vehicleClass', verbose_name='Vehicle Class',on_delete=models.PROTECT)
    locationID = models.ForeignKey('Office', verbose_name='Office', on_delete=models.CASCADE)
    vehiclePhoto = models.ImageField(upload_to='vehicle/', verbose_name='Sample', default='NULL')

    def __str__(self):
        return str('Make: '+ self.make + ' , Model: ' + self.model + ' , Year: ' + self.year + ' , Vin: ' + self.vin + ' , PickUp Office: ' + str(self.locationID))
    class Meta:
        indexes = [models.Index(fields=['make', 'model', 'year', 'locationID'])]

class Invoice(models.Model):
    UNFINISHED = 'U'
    FINISHED = 'F'
    INVOICETYPE = [
        (UNFINISHED, 'U'),
        (FINISHED, 'F')
    ]
    invoiceID = models.AutoField(db_column='INVOICE_ID', primary_key=True)
    firstName = models.CharField(db_column='INVOICE_FIRST_NAME', max_length=50, null=True)
    lastName = models.CharField(db_column='INVOICE_LAST_NAME', max_length=50, null=True)
    invoiceDate = models.DateTimeField(db_column='INVOICE_DATE', auto_now_add=True)
    amount = models.DecimalField(db_column='AMOUNT', max_digits=10, decimal_places=2)
    remainingAmount = models.DecimalField(db_column='REMAIN_AMOUNT', max_digits=10, decimal_places=2, null=True)
    status = models.CharField(db_column='STATUS', max_length=1, choices=INVOICETYPE, default='U')
    def __str__(self):
        return str('ID: ' + str(self.invoiceID) + ' , FirstName: ' + self.firstName
                   + ' , LastName: ' + self.lastName + ' , Date: ' + str(self.invoiceDate.date()) + ' , Status: ' + self.status)
    class Meta:
        indexes = [models.Index(fields=['firstName', 'lastName'])]
class Payment(models.Model):
    CREDITCARD = 'Credit Card'
    DEBITCARD = 'Debit Card'
    GIFTCARD = 'Gift Card'
    PAYMENTMETHOD = [
        (CREDITCARD, 'Credit Card'),
        (DEBITCARD, 'Debit Card'),
        (GIFTCARD, 'Gift Card')
    ]
    paymentID = models.AutoField(db_column='PAYMENT_ID', primary_key=True)
    payMethod = models.CharField(db_column='PAY_METHOD', max_length=50, null=True, choices=PAYMENTMETHOD)
    cardNum = models.CharField(db_column='CARD_NUM', max_length=16, null=True)
    payAmount = models.DecimalField(db_column='PAY_AMOUNT', max_digits=7, decimal_places=2, null=True)
    payDate = models.DateTimeField(db_column='PAY_DATE', auto_now=True)
    invoiceID = models.ForeignKey('Invoice', related_query_name='pay_invoice', on_delete=models.CASCADE)
    def __str__(self):
        return str('paymentID: ' + str(self.paymentID) + ' , Amount: ' + str(self.payAmount) + ' , Invoice: ' + str(self.invoiceID))
    class Meta:
        indexes = [models.Index(fields=['invoiceID'])]


class rentalService(models.Model):
    PENDING = 'P'
    UNPAID = 'U'
    FINISHED = 'F'
    STATUS = [
        (PENDING, 'P'),
        (UNPAID, 'U'),
        (FINISHED, 'F')
    ]
    rsID = models.AutoField(db_column='RSID', primary_key=True)
    customerID = models.ForeignKey('Customer', on_delete=models.CASCADE)
    firstName = models.CharField(db_column='FIRST_NAME', max_length=50, null=True, blank=True)
    lastName = models.CharField(db_column='LAST_NAME', max_length=50, null=True, blank=True)
    pickupDate = models.DateField(db_column='PICKUP_DATE')
    dropoffDate = models.DateField(db_column='DROPOFF_DATE', null=True, blank=True)
    startOdometer = models.DecimalField(db_column='START_ODOMETER', max_digits=7, decimal_places=2, null = True,blank=True)
    endOdometer = models.DecimalField(db_column='END_ODOMETER', max_digits=7, decimal_places=2, null=True, blank=True)
    dailyLimit = models.DecimalField(db_column='DAILY_LIMIT', max_digits=6, decimal_places=2, null=True, blank=True)
    vehicleID = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
    invoiceID = models.ForeignKey('Invoice',related_name='rental_invoice', on_delete=models.PROTECT, blank=True, null=True)
    couponID = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True, blank=True)
    pickupOffice = models.ForeignKey('Office', on_delete=models.CASCADE, null=True, blank=True)
    dropoffOffice = models.ForeignKey('Office', related_name='drop_off', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField('STATUS', max_length=10, choices=STATUS, default='P')
    def __str__(self):
        return str('ID: ' + str(self.rsID) + ' , Customer: ' + str(self.customerID) + ' , Status: ' + self.status)
    class Meta:
        indexes = [models.Index(fields=['customerID'])]






# class pendingService(models.Model):
#     psID = models.AutoField(db_column='PSID', primary_key=True)
#     pickupDate = models.DateField(db_column='PICKUP_DATE')
#     vehicleID = models.ForeignKey('Vehicle', on_delete=models.CASCADE)
#     pickupOffice = models.ForeignKey('Office', on_delete=models.CASCADE)
#     customerID = models.ForeignKey('Customer', on_delete=models.CASCADE)
#     couponID = models.ForeignKey('Coupon', on_delete=models.SET_NULL, null=True)

class userClass(models.Model):
    userID = models.OneToOneField(User, on_delete=models.CASCADE, related_name='Class')
    is_customer = models.BooleanField(db_column='IS_CUSTOMER', default=False)

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            if instance.is_superuser:
                userClass.objects.create(userID=instance, is_customer=False)
            else:
                userClass.objects.create(userID=instance, is_customer=True)
        else:
            obj = userClass.objects.filter(userID=instance).first()
            obj.is_customer = not instance.is_superuser
            obj.save()
            print('test')