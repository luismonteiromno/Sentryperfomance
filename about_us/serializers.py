from .models import AboutUs, TermsOfUse, PrivacyPolice
from rest_framework.serializers import ModelSerializer


class AboutUsSerializer(ModelSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'


class TermsOfUseSerializer(ModelSerializer):
    class Meta:
        model = TermsOfUse
        fields = '__all__'


class PrivacyPoliceSerializers(ModelSerializer):
    class Meta:
        model = PrivacyPolice
        fields = '__all__'
