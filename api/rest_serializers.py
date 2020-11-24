from rest_framework import serializers

class BuildingOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = building_owner
        fields = '__all__'
