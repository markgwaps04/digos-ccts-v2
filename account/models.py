from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, date;
import datetime as date_time
def generate_filename(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext);
    return os.path.join(instance.directory_string_var, filename);
import uuid;
import os;
import random, string
import pdb;
from django.db.models import Sum, Q;
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


# Create your models here.
def filename_generator(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext);
    return os.path.join(instance.directory_string_var, filename);


class ref_region(models.Model):
    id = models.AutoField(primary_key=True);
    psgcCode = models.CharField(max_length=50,blank=False,null=False, unique=True);
    name = models.TextField(blank=False,null=False);
    regCode = models.CharField(max_length=50,blank=False,null=False, unique=True);

    def provinces(self):

        return ref_province\
            .objects\
            .filter(region_id=self.id)\
            .order_by("provCode");

        pass;

    def __str__(self):
        return self.name;
        pass;

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

    pass;

class ref_province(models.Model):
    id = models.AutoField(primary_key=True);
    psgcCode = models.CharField(max_length=50,blank=False,null=False, unique=True);
    name = models.TextField(blank=False,null=False);
    f_region = models.ForeignKey(ref_region, to_field="regCode",on_delete=models.CASCADE, blank=False, null=False);
    region = models.ForeignKey(ref_region,related_name="ref_region_id",on_delete=models.CASCADE, blank=False,
                               null=False);
    provCode = models.CharField(max_length=50,blank=False,null=False,unique=True);

    class Meta:
        verbose_name = _("Province")
        verbose_name_plural = _("Provinces")

    def citymunicipalities(self):

        return ref_citymun\
            .objects\
            .filter(province_id=self.id)\
            .order_by("citymunCode");

        pass;

    def __str__(self):
        return self.name;
        pass;


    pass;


class ref_citymun(models.Model):
    id = models.AutoField(primary_key=True);
    psgcCode = models.CharField(max_length=50,blank=False,null=False, unique=True);
    name = models.TextField(blank=False,null=False);
    f_province = models.ForeignKey(ref_province, to_field="provCode",on_delete=models.CASCADE, blank=False, null=False);
    province = models.ForeignKey(ref_province,related_name="ref_province_id",on_delete=models.CASCADE, blank=False,  null=False);
    citymunCode = models.CharField(max_length=50,blank=False,null=False, unique=True);

    def barangays(self):

        return ref_barangay\
            .objects\
            .filter(citymun_id=self.id)\
            .order_by("brgyCode");

        pass;

    def __str__(self):
        return self.name;
        pass;

    class Meta:
        verbose_name = _("City/Municipality")
        verbose_name_plural = _("Cities and Municipalities")

    pass;


class ref_barangay(models.Model):
    id = models.AutoField(primary_key=True);
    brgyCode = models.CharField(max_length=50,blank=False,null=False, unique=True);
    name = models.TextField(blank=False,null=False);
    f_citymun = models.ForeignKey(ref_citymun, to_field="citymunCode",on_delete=models.CASCADE, blank=False, null=False);
    citymun = models.ForeignKey(ref_citymun,related_name="ref_citymun_id",on_delete=models.CASCADE, blank=False,
                               null=False);


    def __str__(self):
        return self.name;
        pass;

    class Meta:
        verbose_name = _("Barangay")
        verbose_name_plural = _("Barangays")

    pass;


class ref_purok(models.Model):
    id = models.AutoField(primary_key=True);
    name = models.CharField(max_length=50,default="",blank=False,null=False);
    president = models.CharField(max_length=50,default="",blank=True,null=True);
    barangay = models.ForeignKey(ref_barangay,related_name="ref_barangay_id",on_delete=models.CASCADE, blank=False,
                               null=False);
    pass;

class Relationship(models.Model):
    id = models.AutoField(primary_key=True);
    name = models.CharField(max_length=50,default="",blank=False,null=False);
    is_owner = models.BooleanField(blank=False,null=False, default=False)
    pass;

class Reason(models.Model):
    id = models.AutoField(primary_key=True);
    name = models.CharField(max_length=200,default="",blank=False,null=False);
    pass;



class building_owner(models.Model):
    of_gender = [
        (0, 'Male'),
        (1, 'Female')
    ];

    PENDING_VERIFICATION_STATE = 0
    VERIFIED_VERIFICATION_STATE = 1

    account_verification_state = [
        (PENDING_VERIFICATION_STATE, 'Pending'),
        (VERIFIED_VERIFICATION_STATE, 'Verified')
    ];

    confirmation_state = [ (0, 'Pending'), (1, 'Approved'), (2, 'decline')];

    CONFIRM_PENDING = 0;
    CONFIRM_APPROVED = 1;
    CONFIRM_DECLINE = 2;

    directory_string_var = "documents/building_owner";
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=False,null=False);
    establishment_name = models.TextField(blank=False,null=False);
    purok = models.ForeignKey(ref_purok,on_delete=models.CASCADE,blank=False,null=False);
    street = models.CharField(max_length=150,blank=False,null=False);
    verification_file = models.FileField(upload_to=filename_generator, help_text="Select File", blank=False,
                                         null=False);

    profile = models.FileField(upload_to=filename_generator, help_text="Select File", blank=False,
                                         null=True);

    account_is_verified = models.IntegerField(
        blank=False,null=False,choices=account_verification_state,default=PENDING_VERIFICATION_STATE
    );

    date_created= models.DateField(blank=False,null=False,default=date.today);
    is_confirm = models.IntegerField(default=0, blank=False,null=False, choices=confirmation_state);

    def confirm_approved(self):
        self.is_confirm = self.CONFIRM_APPROVED;
        pass;

    def confirm_decline(self):
        self.is_confirm = self.CONFIRM_DECLINE;
        pass;

    def account_type(self):
        return building_owner.__name__;
        pass;

    pass;


class household_profile(models.Model):
    of_gender = [
        (0, 'Male'),
        (1, 'Female')
    ];
    PENDING_VERIFICATION_STATE = 0
    VERIFIED_VERIFICATION_STATE = 1

    directory_string_var = "documents/household";

    account_verification_state = [
        (PENDING_VERIFICATION_STATE, 'Pending'),
        (VERIFIED_VERIFICATION_STATE, 'Verified')
    ];

    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=False,null=False);
    phone_number = models.CharField(max_length=10,blank=False,null=False,unique=True);
    date_of_birth = models.DateField(blank=False,null=False);
    gender = models.BooleanField(blank=False,null=False, choices=of_gender,default=0);
    purok = models.ForeignKey(ref_purok,on_delete=models.CASCADE,blank=False,null=False);
    street = models.CharField(max_length=150,blank=False,null=False);
    verification_file = models.FileField(upload_to=filename_generator, help_text="Select File", blank=False,
                                         null=True);
    profile = models.FileField(upload_to=filename_generator, help_text="Select File", blank=False,
                                         null=True);
    account_is_verified = models.IntegerField(
        blank=False,null=False,choices=account_verification_state,default=PENDING_VERIFICATION_STATE
    );
    date_created= models.DateField(blank=False,null=False,default=date.today);

    def get_age(self):
        today = date_time.date.today();
        birth_year = self.date_of_birth.year;
        return int(today.year) - int(birth_year);
        pass;

    def no_household(self):

        return family_members.objects.filter(
            household_profile_id=self.id,
            is_confirm=True
        ).count();

        pass;

    def account_type(self):
        return household_profile.__name__;
        pass;

    def clean(self):
        self.check_phone_number_is_exists();
        pass;


    def check_phone_number_is_exists(self):

        of_household_exists = household_profile\
            .objects\
            .filter(phone_number=self.phone_number)\
            .exists();

        if of_household_exists:
            raise ValidationError("Phone number not available");

        pass;

    pass;


class family_members(models.Model):
    of_gender = [
        (0, 'Male'),
        (1, 'Female')
    ];
    confirmation_state = [ (0, 'Pending'), (1, 'Approved'), (2, 'decline')];

    CONFIRM_PENDING = 0;
    CONFIRM_APPROVED = 1;
    CONFIRM_DECLINE = 2;

    directory_string_var = "family_members_documents";

    id = models.AutoField(primary_key=True);
    household_profile = models.ForeignKey(household_profile,on_delete=models.CASCADE,blank=False,null=False);
    relationship = models.ForeignKey(Relationship,on_delete=models.CASCADE,blank=False,null=False);
    first_name = models.CharField(max_length=150,blank=False,null=False);
    last_name = models.CharField(max_length=150,blank=False,null=False);
    date_of_birth = models.DateField(blank=False,null=False);
    verification_file = models.FileField(upload_to=filename_generator, help_text="Select documents", blank=False,
                                         null=False);
    profile = models.FileField(upload_to=filename_generator, help_text="Select File", blank=False,
                                         null=True);
    gender = models.BooleanField(blank=False,null=False, choices=of_gender,default=0);
    is_confirm = models.IntegerField(default=0, blank=False,null=False, choices=confirmation_state);
    date_added = models.DateField(blank=False,null=False,default=date.today);

    def get_age(self):
        today = date_time.date.today();
        birth_year = self.date_of_birth.year;
        return int(today.year) - int(birth_year);
        pass;

    def confirm_approved(self):
        self.is_confirm = self.CONFIRM_APPROVED;
        pass;

    def confirm_decline(self):
        self.is_confirm = self.CONFIRM_DECLINE;
        pass;

    def members_like_account(self):

        of_family_members = family_members.objects.filter(
            Q(first_name__icontains=self.first_name),
            Q(last_name__icontains=self.last_name),
            Q(is_confirm=family_members.CONFIRM_APPROVED)
        ).exclude(id=self.id);

        return of_family_members[:5];

        pass;

    pass;






