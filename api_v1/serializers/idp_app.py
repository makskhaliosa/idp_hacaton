from rest_framework import serializers

from idp_app.models import IDP


class IDPSerializer(serializers.ModelSerializer):
    class Meta:
        model = IDP
        fields = "__all__"
