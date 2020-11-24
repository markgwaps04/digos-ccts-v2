from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from modules import helpers
from django.contrib.auth.decorators import login_required, user_passes_test;
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from account.models import building_owner, household_profile
from account.views import should_building_owner,should_not_staff_and_superuser
import random;
import calendar;
import time;
import pdb;

# Create your views here.

def is_email_verified(user):
    building_owner_profile = building_owner.objects.get(user_id=user.id);
    return building_owner_profile.account_is_verified == building_owner_profile.VERIFIED_VERIFICATION_STATE;
    pass;


def should_confirm(user):
    try:
        of_building_owner = building_owner.objects.get(user_id=request.user.id);
        return of_building_owner.is_confirm;
    except building_owner.DoesNotExist:
        return False;
        pass;
    pass;


@login_required(login_url="/")
@user_passes_test(test_func=should_not_staff_and_superuser,login_url="/admin")
@user_passes_test(test_func=should_building_owner,login_url="/")
@user_passes_test(test_func=is_email_verified,login_url="/building_owner/email/verification")
def index(request):
    try:
        of_building_owner = building_owner.objects.get(user_id=request.user.id);

        if of_building_owner.is_confirm == of_building_owner.CONFIRM_PENDING :

            return render(request,"auth/registration_verification_sent.html", {
                "profile" : of_building_owner
            });

        elif of_building_owner.is_confirm == of_building_owner.CONFIRM_APPROVED:

            return render(request,"building_owner/home.html", {
                "profile" : of_building_owner
            });

        else:

            return render(request,"building_owner/decline.html", {
                "profile" : of_building_owner
            });

            pass;

    except building_owner.DoesNotExist:
        request.user.delete();
        pass;


@login_required(login_url="/")
@user_passes_test(test_func=should_not_staff_and_superuser,login_url="/admin")
@user_passes_test(test_func=should_building_owner,login_url="/")
def v_email_verification(request):

    randomlist = random.sample(range(0, 9), 6);
    str_randomlist = "".join([str(i) for i in randomlist]);

    of_building_owner = building_owner.objects.get(user_id=request.user.id);

    if "email_verification" in request.session:
        email_verification = request.session['email_verification'];
        seconds = (int(calendar.timegm(time.gmtime())) - email_verification['timestamp']) / 1000;

        if seconds < 1 :
            return render(request, "auth/registration_email_and_phone_verification.html", {
                "email_params" : email_verification,
                "type" : "household",
                "profile" : of_building_owner
            });
            pass;

    request.session.modified = True;
    request.session['email_verification'] = {
        "value" : str_randomlist,
        "timestamp" : calendar.timegm(time.gmtime())
    }
    request.session.save()

    return render(request, "auth/registration_email_and_phone_verification.html", {
        "email_params" : request.session['email_verification'],
        "type" : "household",
        "profile" : of_building_owner
    })


    pass;



@login_required(login_url="/")
@user_passes_test(test_func=should_not_staff_and_superuser,login_url="/admin")
@user_passes_test(test_func=should_building_owner,login_url="/")
def r_email_verification(request):

    of_building_profile = building_owner.objects.get(user=request.user.id);

    if not "email_verification" in request.session:
        messages.error(request,"Verification code reset", extra_tags="Info");
        return v_email_verification(request);
        pass;

    try:
        constraint = helpers.constraint(request, "POST");
        data = constraint.strict([
            "verification_code"
        ], True);

        email_verification = request.session['email_verification'];

        if not (str(data['verification_code']) == str(email_verification['value'])):
            messages.error(request,"Incorrect verificaton code", extra_tags="Verification code not valid");
            return v_email_verification(request);
            pass;


        of_building_profile.account_is_verified = of_building_profile.VERIFIED_VERIFICATION_STATE;
        of_building_profile.clean();
        of_building_profile.save();

        return redirect("/home");

    except helpers.InvalidRequest:
        messages.info(request,"Please fill all the fields dont leave empty.", extra_tags="Info");
        return v_email_verification(request);

    except Exception as e:
        of_building_profile.account_is_verified = of_building_profile.PENDING_VERIFICATION_STATE;
        of_building_profile.save();
        raise Exception(e);
        pass;

    pass;
