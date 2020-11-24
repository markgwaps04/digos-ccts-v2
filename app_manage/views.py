from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, auth
from django.views.decorators.csrf import csrf_exempt
from modules import helpers
import pdb;

# Create your views here.


@csrf_exempt
def index(request):
    return HttpResponse('Success');
    pass;

@csrf_exempt
def login(request):

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


    if user:
        return HttpResponse("Success")
        pass;

    return AttributeError("Log in details not valid");

    pass;

@csrf_exempt
def scan(request):

    constraint = helpers.constraint(request, "POST");
    data = constraint.strict([
        "scan_result"
    ], True);

    print(data);
    pdb.set_trace();


    pass;
