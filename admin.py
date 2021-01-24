import datetime

from django.contrib import admin, messages
from django.core.checks import Tags
from django.utils.datetime_safe import date
from django.utils.safestring import mark_safe

from func.models import *
from django import forms
admin.site.site_header = 'WOW.COM'    #Set header
admin.site.site_title = 'World on Wheals, Bring Your DreamCar Today!'    #Set title


from django.contrib.admin.models import LogEntry

LogEntry.objects.all().delete()


class indiCustomerAdmin(admin.ModelAdmin):
    list_display = ('customerID',)
    raw_id_fields = ("customerID",)

    def get_queryset(self, request):
        qs = super(indiCustomerAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(customerID=Customer.objects.filter(emailID = request.user).first())

class IndiCustomerTabularInline(admin.TabularInline):
    model=individualCustomer
class CorpCustomerStackedInline(admin.StackedInline):
    model=corporationCustomer


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customerID','emailID','firstName','lastName')
    inlines = [IndiCustomerTabularInline, CorpCustomerStackedInline]

    exclude = ('customerType',)
    def get_queryset(self, request):
        qs = super(CustomerAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        test = Customer.objects.filter(emailID=request.user).first()
        return qs.filter(emailID=test.emailID)
admin.site.register(Customer, CustomerAdmin)




#admin.site.register(individualCustomer, indiCustomerAdmin)


admin.site.register(corporationCustomer)

class vehicleClassAdmin(admin.ModelAdmin):
    list_display = ('type', 'rentCharge', 'extraCharge')

admin.site.register(vehicleClass)
admin.site.register(Office)


class reInline(admin.TabularInline):
    model = rentalService
    #can_delete = False
    fields = ('customerID',)


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('image_data','make','typeID', 'model','year', 'locationID',)
    list_filter = ('make', 'typeID', 'year', 'locationID',)
    list_per_page = 10
    # date_hierarchy = ('make', 'model', 'year',)
    ordering = ('make', 'model', 'year', 'locationID',)
    #exclude = ('vehiclePhoto',)
    readonly_fields = ('image_data',)
    def image_data(self, obj):
        return format_html(
            '<img src="{}" width="100px"/>',
            obj.vehiclePhoto.url
        )
    image_data_short_description = u'Picture'
admin.site.register(Vehicle, VehicleAdmin)


class rsAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (u'Personal Info', {
    #         'fields': ('customerID', 'firstName', 'lastName')
    #     }),
    #     (u'Service Info', {
    #         'fields': ('vehicleID', 'pickupDate', 'dropoffDate','couponID',
    #                    'startOdometer', 'endOdometer', 'dailyLimit', 'pickupOffice', 'dropoffOffice')
    #     }),
    #     (u'Invoice Info', {
    #         'fields': ('invoiceID', 'status', )
    #     }),
    # )
    # readonly_fields = ('dropoffDate', 'startOdometer', 'endOdometer', 'dailyLimit', 'invoiceID', 'dropoffOffice', 'status',)
    #prepopulated_fields = {'pickupOffice'}
    #User for hiding some part from the customer
    def get_queryset(self, request):
        qs = super(rsAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        test = Customer.objects.filter(emailID=request.user).first()
        return qs.filter(customerID=test)
    def get_form(self, request, obj=None, **kwargs):
        self.exclude = []
        if not request.user.is_superuser:
            self.exclude.extend(['pickupOffice','dropoffDate', 'startOdometer', 'endOdometer', 'dailyLimit', 'invoiceID', 'dropoffOffice', 'status'])
        return super(rsAdmin, self).get_form(request, obj, **kwargs)

    #Prevent the user to use other's coupon or order for others.
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        uclass = userClass.objects.filter(userID=request.user)
        if db_field.name == "customerID" and not request.user.is_superuser:    #Only show the user's email address
            kwargs['initial'] = request.user.id
            kwargs["queryset"] = Customer.objects.filter(emailID=request.user)
        if db_field.name == "couponID" and not request.user.is_superuser:    #For only show the coupon that user owns
            cust = Customer.objects.filter(emailID = request.user).first()
            cust_cou = Coupon_Customer.objects.filter(customerID = cust)
            list = []
            for c in cust_cou:
                list.append(c.couponID.couponID)
            kwargs["queryset"] = Coupon.objects.filter(couponID__in=list)

        return super(rsAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        uclass = userClass.objects.filter(userID=request.user).first()
        cust = Customer.objects.filter(emailID=request.user.username).first()
        if uclass.is_customer:    #Just save
            obj.customerID = cust
            vehicle = obj.vehicleID
            office = vehicle.locationID
            obj.pickupOffice = office
            if obj.couponID is not None:
                coupon = obj.couponID
                couponList = Coupon_Customer.objects.filter(customerID=cust, couponID=obj.couponID)
                if not coupon.is_corp:
                    now = datetime.datetime.date(datetime.datetime.now())
                    if coupon.validFrom > now or coupon.validTo < now:
                        messages.error(request, " Coupon is not vaild!! Please check the valid time!")
                        messages.set_level(request, messages.ERROR)
                    if couponList is not None:
                        couponList.delete()
                #else:
            super().save_model(request, obj, form, change)
        else:    #If employee
            if obj.status == 'U':    #
                vid = obj.vehicleID.typeID
                veClass = vehicleClass.objects.filter(typeID=vid.typeID).first()
                coupon = 0
                if obj.couponID is not None:
                    coupon = obj.couponID.discount
                days = (obj.dropoffDate-obj.pickupDate).days
                meter = obj.endOdometer - obj.startOdometer
                extraPart = 0
                if obj.dailyLimit is None:
                    extraPart = 0
                else:
                    extraPart = (meter - days*obj.dailyLimit)*veClass.extraCharge
                amount = (1-coupon)*(veClass.rentCharge * (days)+extraPart)    #Total Fee Calculation
                if obj.invoiceID is None or Invoice.objects.filter(invoiceID=obj.invoiceID.invoiceID) is None:
                    # obj.firstName = obj.customerID.firstName
                    # obj.lastName = obj.customerID.lastName
                    invoice = Invoice.objects.create(firstName=obj.firstName, lastName=obj.lastName, amount=amount, status='U', remainingAmount=amount, )
                    obj.invoiceID = invoice
                else:
                    invoice = Invoice.objects.filter(invoiceID=obj.invoiceID.invoiceID).first()
                    invoice.remainingAmount = (amount - invoice.amount) + invoice.remainingAmount
                    invoice.amount = amount
                    invoice.save()
                super().save_model(request, obj, form, change)
            elif obj.status == 'P':
                messages.error(request, " Please set the STATUS into Unpaid！" )
                messages.set_level(request, messages.ERROR)
            else:
                messages.error(request, " Service finished. It's unchangeable！")
                messages.set_level(request, messages.ERROR)
admin.site.register(rentalService, rsAdmin)


class couponAdmin(admin.ModelAdmin):
    list_display = ('couponID', 'discount', 'validFrom', 'validTo')
    def get_queryset(self, request):
        qs = super(couponAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        cusID = Customer.objects.filter(emailID=request.user).first()
        test = Coupon_Customer.objects.filter(customerID=cusID)
        list = []
        for t in test:
            list.append(t.couponID.couponID)
        return qs.filter(couponID__in = list)

admin.site.register(Coupon, couponAdmin)


class coupon_customerAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):    #Prevent the employee add the corporation coupon to wrong corporation user
        coupon = obj.couponID
        customer = obj.customerID
        if coupon.is_corp:
            cus_corp = corporationCustomer.objects.filter(customerID=customer).first()
            cou_corp = coupon.corporation
            if cus_corp is None or cou_corp is None or cus_corp.corporationID != cou_corp:
                messages.error(request, " Corporation not matched!!")
                messages.set_level(request, messages.ERROR)
            else:
                super().save_model(request, obj, form, change)
        else:
            super().save_model(request, obj, form, change)

admin.site.register(Coupon_Customer, coupon_customerAdmin)

class invoiceAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields': ( 'firstName', 'lastName',  'amount',
    #                    'remainingAmount', 'status',)
    #     }),
    #
    # )
    def get_queryset(self, request):
        qs = super(invoiceAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        test = Customer.objects.filter(emailID=request.user).first()
        rsQuery = rentalService.objects.filter(customerID = test)
        list = []
        for r in rsQuery:
            if r.invoiceID is not None:
                list.append(r.invoiceID.invoiceID)
        return qs.filter(pk__in=list)
admin.site.register(Invoice, invoiceAdmin)

class paymentAdmin(admin.ModelAdmin):
    # fieldsets = (
    #     (None, {
    #         'fields': ('paymentID', 'payMethod', 'cardNum', 'payAmount', 'payDate',
    #                    'invoiceID',)
    #     }), )
    def get_queryset(self, request):
        qs = super(paymentAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        test = Customer.objects.filter(emailID=request.user).first()
        rsQuery = rentalService.objects.filter(customerID=test)
        list = []
        for r in rsQuery:
            list.append(r.invoiceID)
        return qs.filter(invoiceID__in = list)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "invoiceID" and not request.user.is_superuser:
            #kwargs['initial'] = request.rentalService.customerID
            custMid = Customer.objects.filter(emailID = request.user).first()
            rentalMid = rentalService.objects.filter(customerID = custMid).filter(status = 'U')
            list = []
            for e in rentalMid:
                list.append(e.invoiceID.invoiceID)
            kwargs["queryset"] = Invoice.objects.filter(pk__in = list).filter(status='U')
        return super(paymentAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    def save_model(self, request, obj, form, change):
        invoice = obj.invoiceID
        remainAmount = invoice.remainingAmount
        if invoice.status == 'F':
            messages.error(request, " Transaction Closed")
            messages.set_level(request, messages.ERROR)
        else:
            amount = obj.payAmount
            if(invoice.remainingAmount - amount < 0):
                messages.error(request, "Too much money!!! Please reenter the amount!")
                messages.set_level(request, messages.ERROR)
            else:
                if(invoice.remainingAmount - amount  == 0):
                    invoice.status = 'F'
                    rental = rentalService.objects.filter(invoiceID = invoice)
                    rental.status = 'F'
                invoice.remainingAmount = invoice.remainingAmount - amount
                invoice.save()
                super().save_model(request, obj, form, change)

admin.site.register(Payment, paymentAdmin)

admin.site.register(userClass)

admin.site.register(Corporation)