from django import forms;
from account.models import \
    building_owner, \
    family_members, \
    household_profile

class BuildingOwnerForm(forms.ModelForm):

    class Meta:
        model = building_owner;
        fields = [
            'user',
            'establishment_name',
            'purok',
            'street',
            'verification_file',
            'profile'
        ]

    pass;

class HouseholdForm(forms.ModelForm):

    class Meta:
        model = household_profile;
        fields = [
            'user',
            'phone_number',
            'account_is_verified',
            'date_of_birth',
            'gender',
            'purok',
            'street',
            'verification_file',
            'profile'
        ]

    pass;



class FamilyMembersForm(forms.ModelForm):

    class Meta:
        model = family_members;
        fields = [
            'household_profile',
            'relationship',
            'first_name',
            'last_name',
            'date_of_birth',
            'verification_file',
            'profile',
            'is_confirm'
        ]

    pass;
