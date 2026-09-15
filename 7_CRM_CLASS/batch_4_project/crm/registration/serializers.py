from rest_framework import serializers
from .models import Registration


# Serializer converts Registration model data to JSON,
# and also converts JSON data back to Registration model data.
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        # Which model this serializer will work with.
        model = Registration

        # Which model fields will be shown/accepted in the API.
        fields = ['id', 'name', 'email', 'password', 'date_of_birth']
