from rest_framework import serializers
from .models import Indicator, MonthlyFormHeader, MonthlyFormLine, Company

class IndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicator
        fields = '__all__'

class MonthlyFormHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyFormHeader
        fields = '__all__'

class MonthlyFormLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyFormLine
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'