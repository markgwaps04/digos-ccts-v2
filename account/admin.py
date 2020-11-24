from django.contrib import admin
from account.models import building_owner, \
    household_profile,\
    ref_province, \
    ref_citymun, \
    ref_barangay, \
    ref_region, \
    ref_purok, \
    Relationship, \
    Reason


@admin.register(Relationship)
class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    search_fields = (
        'id',
        'name',
        "is_owner"
    )

@admin.register(Reason)
class ReasonAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    search_fields = (
        'id',
        'name'
    )



@admin.register(ref_purok)
class PurokAdmin(admin.ModelAdmin):
    list_display = ('id','barangay', 'name', 'president')
    search_fields = ('id','barangay', 'name', 'president')


@admin.register(ref_barangay)
class BarangayAdmin(admin.ModelAdmin):
    list_display = ('id','brgyCode', 'name','citymun')
    search_fields = ('id','brgyCode', 'name','citymun')


# @admin.register(Municipalities)
# class MunicipalityAdmin(admin.ModelAdmin):
#     list_display = ('id','name')
#     search_fields = ('id','name')
