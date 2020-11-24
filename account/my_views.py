from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from modules import helpers
from django.contrib.auth.decorators import login_required, user_passes_test;
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.models import Group
from account.views import Category
from account.models import building_owner, \
    household_profile,\
    ref_province, ref_citymun, ref_barangay, ref_region, ref_purok
from account.forms import BuildingOwnerForm, \
    HouseholdForm
from django.db.models import Sum, Q;
from django.core import serializers
import pdb;
import random
from django.conf import settings
import requests
import json;
from django.db.models import QuerySet
from django.conf import settings


def should_not_log_in(user):

    return (not user.is_authenticated) or user.is_superuser;
    pass;


@user_passes_test(test_func=should_not_log_in, login_url="/home")
def login(request):
    return render(request, "auth/login.html");
    pass;


@user_passes_test(test_func=should_not_log_in, login_url="/home")
def r_login_request(request):

    try:
        constraint = helpers.constraint(request, "POST");
        data = constraint.strict([
            "username",
            "password"
        ], True);

        user = auth.authenticate(
            username=data['username'],
            password=data['password'],
            is_staff = False,
            is_superuser=False
        );

        if user and not user.is_superuser:
            auth.login(request, user);
            return redirect("/home");

        messages.error(request,
                       "Username and Password do not match. Please try again."
                       "if username and password do not work your account may have been disabled",
                       extra_tags="Account not found");
        return login(request);

    except helpers.InvalidRequest:
        messages.error(request,
                       "Please dont leave blanks before submitted"
                       " (Palihug ayaw ibilin ang mga blangko sa wala pa isumite)",
                       extra_tags="Request not valid");
        return login(request);



    pass;



@user_passes_test(test_func=should_not_log_in, login_url="/home")
def v_register_as_building_owner(request):
    of_purok = Purok.objects.all().order_by("barangay__name", "name");

    return render(request, "auth/sign_up_as_building_owner.html",
                  {
                      "purok": of_purok,
                      "gender": building_owner.of_gender,
                      "data": request.POST
                  });
    pass;


@user_passes_test(test_func=should_not_log_in, login_url="/home")
def r_register_as_building_owner(request):
    try:

        constraint = helpers.constraint(request, "POST");
        data = constraint.strict([
            "establishment_email",
            "username",
            "password",
            "establishment_name",
            "establishment_street",
            "establishment_purok"
        ], True);

        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=values)
        result = r.json()
        ''' End reCAPTCHA validation '''

        if not result['success']:
            messages.error(request,"Invalid recaptcha",extra_tags="Request not valid");
            raise helpers.InvalidRequest("Household profile invalid params");
            pass;

        user = User.objects.create_user(
            email=data['establishment_email'],
            username=data['username'],
            password=data['password'],
            is_staff=False
        );

        my_group = Group.objects.get(id=Category.group_building_owner_id);
        my_group.user_set.add(user);

        that_building_owner_data = {
            "user": user.id,
            "establishment_name": data['establishment_name'],
            "purok": data['establishment_purok'],
            "street": data['establishment_street']
        };

        form = BuildingOwnerForm(data=that_building_owner_data, files=request.FILES);
        validate = form.is_valid();

        if not validate:
            user.delete();
            raise helpers.InvalidRequest("Establishment profile not valid");

        edit = form.save(commit=True);
        edit.save();

        user = auth.authenticate(
            username=data['username'],
            password=data['password']
        );

        auth.login(request, user);

        return redirect("/home");

    except helpers.InvalidRequest:
        messages.error(request,
                       "Please dont leave blanks before submitted"
                       " (Palihug ayaw ibilin ang mga blangko sa wala pa isumite)",
                       extra_tags="Request not valid");
        return v_register(request);

    except UnboundLocalError as e:

        messages.error(request,
                       "Please dont leave blanks before submitted"
                       " (Palihug ayaw ibilin ang mga blangko sa wala pa isumite)",
                       extra_tags="Request not valid");
        return v_register(request);

        pass;

    except Exception as e:
        if user: user.delete();
        raise Exception(e);

    pass;

    pass;

@user_passes_test(test_func=should_not_log_in, login_url="/home")
def r_check_phone_number_is_exists(request):

    constraint = helpers.constraint(request, "GET");
    data = constraint.strict([
        "phone_number"
    ], True);

    data['phone_number'] = "".join([char for char in data['phone_number'] if char.isalnum()]);

    of_household_exists = household_profile\
        .objects\
        .filter(phone_number=data['phone_number'])\
        .exists();

    if of_household_exists:
        raise helpers.PhoneNumberAlreadyExists("Phone number not available");

    return HttpResponse('');

    pass;


@user_passes_test(should_not_log_in, redirect_field_name="/home")
def r_check_username_exist(request):

    constraint = helpers.constraint(request, "GET");
    data = constraint.strict([
        "username"
    ], True);

    of_exists = User\
        .objects\
        .filter(username=data['username'])\
        .exists();

    if of_exists:
        raise helpers.UsernameAlreadyExists("Phone number not available");

    return HttpResponse('');

    pass;


@user_passes_test(should_not_log_in, redirect_field_name="/home")
def v_register(request):

    of_province = ref_province.objects.all().order_by("provCode");

    of_barangay = ref_barangay\
        .objects\
        .filter(f_citymun_id=settings.DEFAULT_MUNICIPALITY_CODE)\
        .order_by("name");

    return render(request, "auth/register.html",
                  {
                      "province" : of_province,
                      "barangay": of_barangay,
                      # "municipalities" : of_municipalities,
                      "gender": building_owner.of_gender,
                      "data": request.POST,
                      "category" : Category,
                      "GOOGLE_RECAPTCHA_SITE_KEY" : settings.GOOGLE_RECAPTCHA_SITE_KEY
                  });

    pass;

@user_passes_test(should_not_log_in, redirect_field_name="/home")
def r_register_household(request):

    try:
        constraint = helpers.constraint(request, "POST");
        data = constraint.strict([
            "resident_first_name",
            "resident_last_name",
            "phone_number",
            "username",
            "resident_password",
            "resident_date_of_birth",
            "resident_gender",
            "resident_purok",
            "resident_street",
        ], True);

        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=values)
        result = r.json()
        ''' End reCAPTCHA validation '''

        if not result['success']:
            messages.error(request,"Invalid recaptcha",extra_tags="Request not valid");
            raise helpers.InvalidRequest("Household profile invalid params");
            pass;

        user = User.objects.create_user(
            username=data['username'],
            password=data['resident_password'],
            first_name=data['resident_first_name'],
            last_name=data['resident_last_name'],
            is_staff=False
        );

        my_group = Group.objects.get(id=Category.group_citizens_id);
        my_group.user_set.add(user);

        of_purok = Purok.objects.get(id=data['resident_purok']);

        data['phone_number'] = "".join([char for char in data['phone_number'] if char.isalnum()]);

        household_form_params = {
            "user": user,
            "phone_number" : data['phone_number'],
            "date_of_birth" : data['resident_date_of_birth'],
            "gender" : data['resident_gender'],
            "purok" : of_purok,
            "account_is_verified" : household_profile.PENDING_VERIFICATION_STATE,
            "street" : data['resident_street']
        }

        of_household_profile = HouseholdForm(data=household_form_params,files=request.FILES);

        validate_household_profile = of_household_profile.is_valid();

        if not validate_household_profile:
            user.delete();
            raise helpers.InvalidRequest("Household profile invalid params");

        edit = of_household_profile.save(commit=True);
        edit.save();

        user = auth.authenticate(
            username=data['username'],
            password=data['resident_password']
        );

        auth.login(request, user);

        return redirect("/home");

    except helpers.InvalidRequest:
        messages.error(request,
                       "Please dont leave blanks before submitted"
                       " (Palihug ayaw ibilin ang mga blangko sa wala pa isumite)",
                       extra_tags="Request not valid");
        return v_register_household(request);

    except UnboundLocalError as e:

        messages.error(request,
                       "Please dont leave blanks before submitted"
                       " (Palihug ayaw ibilin ang mga blangko sa wala pa isumite)",
                       extra_tags="Request not valid");
        return v_register(request);

        pass;

    except Exception as e:
        if user: user.delete();
        raise Exception(e);

    pass;

@user_passes_test(should_not_log_in, redirect_field_name="/home")
def get_puroks_from_barangay(request):

    constraint = helpers.constraint(request, "GET");
    data = constraint.strict([
        "barangay"
    ], True);

    of_barangay = ref_barangay.objects.get(id=data['barangay']);

    of_purok = ref_purok.objects.filter(barangay=of_barangay);

    qs_json = serializers.serialize('json', of_purok);

    return HttpResponse(qs_json, content_type='application/json');

@user_passes_test(should_not_log_in, redirect_field_name="/home")
def v_register_validate_phone_number(request):
    return HttpResponse("Success");
    pass;
