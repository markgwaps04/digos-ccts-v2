from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User, auth
from api.custom_exceptions import AuthenticationFailed, \
    BuildingOwnerNotFound, \
    ParametersNotValid, \
    InnerException, \
    AccountNotVerified
from account.models import building_owner
from rest_framework import serializers
from modules import helpers
import pdb;

# Create your views here.

class BuildingOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = building_owner
        fields = '__all__'


@api_view(['GET'])
def index(request):

    api_urls = {
        "List" : "/building-owner/",
        "Insert Log" : "/create-log/<str:pk>",
        "Establishment authentication" : "establishment/<str:username>"
    }
    return Response(api_urls);
    pass;

@api_view(['POST'])
def establishment_auth(request, username, format=None):

    try:

        constraint = helpers.constraint(request, "POST");
        data = constraint.strict([
            "auth.pass"
        ], True);

        user = auth.authenticate(
            username=username,
            password=data['auth.pass'],
            is_staff = False,
            is_superuser=False
         );

        if not user :
            raise AuthenticationFailed();


        of_building_owner = building_owner.objects.get(
            user_id=user.id
        );

        if not of_building_owner.account_is_verified:
            raise AccountNotVerified();

        serializer = BuildingOwnerSerializer(of_building_owner, many=False)
        return Response(serializer.data);

    except helpers.InvalidRequest:
        raise ParametersNotValid();
        pass;
    except building_owner.DoesNotExist as e :
        raise BuildingOwnerNotFound();
        pass;


    pass;
