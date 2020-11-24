from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test;
from account.views import \
    Category, \
    should_not_staff_and_superuser, \
    should_superuser;
from account.models import  building_owner, family_members, Reason
from modules import helpers
from app.settings import MEDIA_URL
import pdb;

# Create your views here.

@login_required(login_url="/")
@user_passes_test(test_func=should_superuser,login_url="/home")
def index(request):

    return render(request,"web_manage/web_manage_home.html",{
        "building_request" : building_owner.objects.filter(is_confirm=False).count(),
        "household_request" : family_members.objects.filter(is_confirm=False).count()
    });
    pass;



@login_required(login_url="/")
@user_passes_test(test_func=should_superuser,login_url="/home")
def household_request(request):

    return render(request,"web_manage/web_manage_household.html",{
        "household_request" : family_members.objects.filter(is_confirm=False).count()
    });
    pass;


@login_required(login_url="/")
@user_passes_test(test_func=should_superuser,login_url="/home")
def household_populate_request(request):

    of_list = family_members\
        .objects\
        .filter(is_confirm=family_members.CONFIRM_PENDING)\
        .order_by("-id")

    of_reason = Reason.objects.all().order_by("name");

    return render(request,"web_manage/load_ajax/household_populate_list.html",{
        "data" : of_list,
        "reason" : of_reason,
        "itemCount" : len(of_list)
    });
    pass;



@login_required(login_url="/")
@user_passes_test(test_func=should_superuser,login_url="/home")
def changed_state_members_request(request):

    constraint = helpers.constraint(request, "POST");
    data = constraint.strict([
        "family_members_id",
        "state"
    ], True);

    data['state'] = "confirm_" + str(data['state']);

    of_members = family_members.objects.get(id=data['family_members_id']);
    check_if_valid_action = hasattr(of_members, data['state']);

    if not check_if_valid_action: raise helpers.InvalidRequest("Parameter 'state' not valid action");

    of_method = getattr(of_members, data['state'])();

    of_members.save();

    return render(request,"web_manage/load_ajax/household_respond_state.html",{
        "data" : of_members
    });


@login_required(login_url="/")
@user_passes_test(test_func=should_superuser,login_url="/home")
def view_establishment_request(request):
    return render(request,"web_manage/web_manage_establishment.html",{
        "household_request" : family_members.objects.filter(is_confirm=False).count()
    });
    pass;



@login_required(login_url="/")
@user_passes_test(test_func=should_superuser,login_url="/home")
def establishment_populate_request(request):

    of_list = building_owner\
        .objects\
        .filter(is_confirm=building_owner.CONFIRM_PENDING);

    of_reason = Reason.objects.all().order_by("name");

    return render(request,"web_manage/load_ajax/establishment_populate_list.html",{
        "data" : of_list,
        "reason" : of_reason,
        "itemCount" : len(of_list)
    });
    pass;


@login_required(login_url="/")
@user_passes_test(test_func=should_superuser,login_url="/home")
def establishment_state_change_request(request):

    constraint = helpers.constraint(request, "POST");
    data = constraint.strict([
        "establishment_id",
        "state"
    ], True);

    data['state'] = "confirm_" + str(data['state']);

    of_members = building_owner.objects.get(id=data['establishment_id']);
    check_if_valid_action = hasattr(of_members, data['state']);

    if not check_if_valid_action: raise helpers.InvalidRequest("Parameter 'state' not valid action");

    of_method = getattr(of_members, data['state'])();

    of_members.full_clean();
    of_members.clean();
    of_members.save();

    return render(request,"web_manage/load_ajax/establishment_respond_state.html",{
        "data" : of_members
    });

    pass;
