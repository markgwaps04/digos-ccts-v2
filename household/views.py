from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from modules import helpers
from django.contrib.auth.decorators import login_required, user_passes_test;
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout
from account.models import building_owner, household_profile, Relationship, family_members
from account.forms import FamilyMembersForm
from account.views import should_household, \
    should_not_staff_and_superuser
from PIL import Image, ImageFont, ImageDraw;
from io import BytesIO
from django.template.loader import get_template
import io;
from app.settings import STATIC_URL;
import xhtml2pdf.pisa as pisa
import base64
import json
import pdb;
import datetime;
import qrcode
import random
import calendar;
import time;
from django.db.models import Sum, Q;

def is_phone_number_verified(user):
    of_household_profile = household_profile.objects.get(user_id=user.id);
    return of_household_profile.account_is_verified == of_household_profile.VERIFIED_VERIFICATION_STATE;
    pass;

def is_account_pending(user):
    of_household_profile = household_profile.objects.get(user_id=user.id);
    return of_household_profile.account_is_verified == of_household_profile.PENDING_VERIFICATION_STATE;
    pass;

# Create your views here.

@login_required(login_url="/")
@user_passes_test(test_func=should_not_staff_and_superuser, login_url="/admin")
@user_passes_test(test_func=should_household, login_url="/")
@user_passes_test(test_func=is_phone_number_verified, login_url="/household/phone_number/verification")
def index(request):
    return render(request, "household/home.html");
    pass;


@login_required(login_url="/")
@user_passes_test(test_func=should_not_staff_and_superuser, login_url="/admin")
@user_passes_test(test_func=should_household, login_url="/")
@user_passes_test(test_func=is_account_pending, login_url="/household/home")
def v_phone_number_verification(request):
    #Generate 5 random numbers between 10 and 30

    of_household_profile = household_profile.objects.get(user=request.user.id);

    randomlist = random.sample(range(0, 9), 5);
    str_randomlist = "".join([str(i) for i in randomlist]);

    if "sms_verification" in request.session:
        sms_verification = request.session['sms_verification'];
        seconds = (int(calendar.timegm(time.gmtime())) - sms_verification['timestamp']) / 1000;

        if seconds < 1 :
            return render(request, "auth/registration_email_and_phone_verification.html", {
                "sms_params" : sms_verification,
                "type" : "household",
                "profile" : of_household_profile
            })
            pass;

    request.session.modified = True;
    request.session['sms_verification'] = {
        "value" : str_randomlist,
        "timestamp" : calendar.timegm(time.gmtime())
    }
    request.session.save()

    return render(request, "auth/registration_email_and_phone_verification.html", {
        "sms_params" : request.session['sms_verification'],
        "type" : "household",
        "profile" : of_household_profile
    })

    pass;


@login_required(login_url="/")
@user_passes_test(test_func=should_not_staff_and_superuser, login_url="/admin")
@user_passes_test(test_func=should_household, login_url="/")
@user_passes_test(test_func=is_account_pending, login_url="/household/home")
def r_phone_number_verification(request):

    of_household_profile = household_profile.objects.get(user=request.user.id);

    if not "sms_verification" in request.session:
        messages.error(request,"Verification code reset", extra_tags="Info");
        return v_phone_number_verification(request);
        pass;

    try:
        constraint = helpers.constraint(request, "POST");
        data = constraint.strict([
            "verification_code"
        ], True);

        sms_verification = request.session['sms_verification'];
        print(sms_verification);

        if not (str(data['verification_code']) == str(sms_verification['value'])):
            messages.error(request,"Incorrect verificaton code", extra_tags="Verification code not valid");
            return v_phone_number_verification(request);
            pass;

        of_household_profile.account_is_verified = of_household_profile.VERIFIED_VERIFICATION_STATE;
        of_household_profile.clean();
        of_household_profile.save();

        of_family_member = family_members(
            household_profile = of_household_profile,
            relationship = Relationship.objects.get(is_owner=True),
            first_name = of_household_profile.user.first_name,
            last_name = of_household_profile.user.last_name,
            date_of_birth = of_household_profile.date_of_birth,
            gender = of_household_profile.gender,
            verification_file = of_household_profile.verification_file,
            profile = of_household_profile.profile
        );

        of_family_member.clean();
        of_family_member.save();

        return redirect("/home");

    except helpers.InvalidRequest:
        messages.info(request,"Please fill all the fields dont leave empty.", extra_tags="Info");
        return v_phone_number_verification(request);

    except Exception as e:
        of_household_profile.account_is_verified = of_household_profile.PENDING_VERIFICATION_STATE;
        of_household_profile.save();
        raise Exception(e);
        pass;

    pass;

@login_required(login_url="/")
@user_passes_test(test_func=should_not_staff_and_superuser, login_url="/admin")
@user_passes_test(test_func=should_household, login_url="/")
@user_passes_test(test_func=is_phone_number_verified, login_url="/household/phone_number/verification")
def family(request):
    of_household_profile = household_profile.objects.get(user=request.user.id);
    of_family_members = family_members \
        .objects \
        .filter(household_profile_id=of_household_profile.id) \
        .exclude(is_confirm=family_members.CONFIRM_DECLINE)\
        .order_by("-id");

    relationships = Relationship.objects.all().order_by("name");

    has_owner_in_choices = of_family_members\
        .filter(relationship__is_owner=True,
                is_confirm=family_members.CONFIRM_APPROVED)\
        .exists()

    if has_owner_in_choices :
        relationships = Relationship.objects.filter(is_owner=False).order_by("name");
        pass;

    return render(request, "household/family.html", {
        "relationship": relationships,
        "household_profile": of_household_profile,
        "family_members": of_family_members
    });

    pass;


@login_required(login_url="/")
@user_passes_test(test_func=should_not_staff_and_superuser, login_url="/admin")
@user_passes_test(test_func=should_household, login_url="/")
@user_passes_test(test_func=is_phone_number_verified, login_url="/household/phone_number/verification")
def r_add_family_members(request):
    try:
        constraint = helpers.constraint(request, "POST");
        data = constraint.strict([
            "household_profile",
            "first_name",
            "last_name",
            "date_of_birth",
            "relationship",
            "gender"
        ], True);

        of_household_profile = household_profile.objects.get(
            id=data['household_profile'],
            user=request.user
        );

        of_relationship = Relationship.objects.get(id=data['relationship']);

        data['is_confirm'] = family_members.CONFIRM_PENDING;

        form = FamilyMembersForm(data=data, files=request.FILES);
        validate = form.is_valid();

        if not validate:
            print(form.errors);
            raise helpers.InnerInvalidRequest();

        form.save();

        of_message = " ".join([
            "you have sent a request to verify.",
            "Please wait for our respond for this matter"
        ]);

        messages.success(request, of_message, extra_tags="Successfully added");
        return redirect("/household/family")

    except helpers.InvalidRequest:
        messages.error(request,
                       "Please dont leave blanks before submitted"
                       " (Palihug ayaw ibilin ang mga blangko sa wala pa isumite)",
                       extra_tags="Request not valid");
        return family(request);

    except helpers.InnerInvalidRequest:
        messages.error(request,
                       "Inner validition result invalid",
                       extra_tags="Request valid but parameters not satisfy");
        return family(request);

    except household_profile.DoesNotExist:

        messages.error(request, "household_profile id does not valid or not exits", extra_tags="Request not valid");
        return family(request);

        pass;

    except Relationship.DoesNotExist:

        messages.error(request, "Relationship id does not valid or not exits", extra_tags="Request not valid");
        return family(request);

        pass;

    except Exception as e:
        raise Exception(e);
    pass;


def generate_id_card(request):
    constraint = helpers.constraint(request, "GET");
    data = constraint.strict([
        "family_members_id"
    ], True);

    of_members = family_members.objects.get(
        id=data['family_members_id'],
        is_confirm=family_members.CONFIRM_APPROVED
    );

    json_returne = {
        "id": of_members.id
    };

    json_object = json.dumps(json_returne, indent=None, separators=(",", ":"));
    format_data = base64.b64encode(bytes(str(json_object), 'utf-8'));

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=20,
        border=0,
    )
    qr.add_data(format_data)
    qr.make(fit=True)

    img_qr_code = qr.make_image(fill_color="black", back_color="white");

    path_image_format = "static/images/id_card.jpg";
    path_image_back_format = "static/images/id_card_back.jpg";

    path_arial_italic = "static/font/Arial Italic.ttf";


    img = Image.open(path_image_format);
    img_back = Image.open(path_image_back_format);
    draw = ImageDraw.Draw(img);
    draw_back = ImageDraw.Draw(img_back);

    font = ImageFont.truetype("arial", 25);
    font_italic = ImageFont.truetype(path_arial_italic, 20);

    birth_date = of_members.household_profile.date_of_birth.strftime("%B %d %Y");

    full_name = " ".join([of_members.first_name, of_members.last_name]);
    address = "".join([of_members.household_profile.purok.name, ", Digos City"]);
    age_birthdate = " ".join([str(of_members.household_profile.get_age()), ", ", birth_date]);

    draw.text((187, 273), full_name, (0, 0, 0), font=font)

    draw.text((220, 310), address, (0, 0, 0), font=font)

    if of_members.household_profile.purok.barangay:
        draw.text((233, 348), of_members.household_profile.purok.barangay.name, (0, 0, 0), font=font);
    else:
        draw.text((233, 348), "(Not specified)", (0, 0, 0), font=font_italic);

    draw.text((373, 385), "23, April 11 1997", (0, 0, 0), font=font);

    #__________________________________________________________
    #Back

    img_qr_w, img_qr_h = img_qr_code.size;
    img_back_w, img_back_h = img_back.size

    # offset = ((img_back_w - img_qr_w) // 2, (img_back_h - img_qr_h) // 2);

    j = 100, 100

    img_back.paste(img_qr_code, j )

    buff = BytesIO()
    buff2 = BytesIO()
    img.save(buff, "PNG")
    img_back.save(buff2, "PNG")
    img_str = base64.b64encode(buff.getvalue());
    img_back = base64.b64encode(buff2.getvalue());
    buff.close();
    buff2.close()

    template = get_template("household/id_card.html");

    html = template.render({
        "img_front": img_str.decode('utf-8'),
        "img_back" : img_back.decode('utf-8'),
    });

    ts = datetime.datetime.now().timestamp();
    file_name = "PHIL-IRI_" + str(ts) + ".zip";

    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), response)
    if not pdf.err:
        on_print = HttpResponse(response.getvalue(), content_type='application/zip');
        on_print['Content-Disposition'] = 'attachment; filename=' + file_name;
        return on_print;
    else:
        return HttpResponse("Error Rendering PDF", status=400)

    # return render(request, "household/id_card.html", {
    #     "img_front": img_str.decode('utf-8')
    # });

pass;


@login_required(login_url="/")
@user_passes_test(test_func=should_not_staff_and_superuser, login_url="/admin")
@user_passes_test(test_func=should_household, login_url="/")
@user_passes_test(test_func=is_phone_number_verified, login_url="/household/phone_number/verification")
def qr_code(request):
    constraint = helpers.constraint(request, "GET");
    data = constraint.strict([
        "family_members_id"
    ], True);

    of_members = family_members.objects.get(id=data['family_members_id']);

    json_returne = {
        "id": of_members.id
    };

    json_object = json.dumps(json_returne, indent=None, separators=(",", ":"));
    format_data = base64.b64encode(bytes(str(json_object), 'utf-8'));

    return render(request, "household/qr_code.html", {
        "format_data": format_data
    });

    pass;

@login_required(login_url="/")
@user_passes_test(test_func=should_not_staff_and_superuser, login_url="/admin")
@user_passes_test(test_func=should_household, login_url="/")
@user_passes_test(test_func=is_phone_number_verified, login_url="/household/phone_number/verification")
def cancel_request_adding_family_members(request):

    constraint = helpers.constraint(request, "GET");
    data = constraint.strict([
        "family_members_id"
    ], True);

    of_family_members = family_members.objects.get(
        id=data['family_members_id'],
        household_profile__user_id=request.user.id
    );

    of_family_members.delete();

    return redirect('/household/family');


    pass;
