from .models import AboutUs, TermsOfUse
from rest_framework.serializers import ModelSerializer


class AboutUsSerializer(ModelSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'


class TermsOfUseSerializer(ModelSerializer):
    class Meta:
        model = TermsOfUse
        fields = '__all__'
