from rest_framework import serializers

from django.contrib.auth import get_user_model
User = get_user_model()

class FloatDecimalField(serializers.DecimalField):
    def to_representation(self, value):
        return float(value)

class UserSerializer(serializers.ModelSerializer):
    height = FloatDecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = User
        fields = ['email', 'gender', 'date_of_birth', 'weight', 'height']