from rest_framework import serializers
from .models import Registration # Importing the registration model class from the models.py
# Lets check the crm/registration/models.py 

from django.contrib.auth import authenticate, get_user_model # get_user_model gets djangos user model, authenticate-> checks passowrd
from rest_framework_simplejwt.tokens import RefreshToken # creates refresh and access token.
# without them, serializer can not check login credentials or create jwt

# Serializer converts Registration model data to specific JSON,
# and also converts JSON data back to specific Registration model data.
# It actually works as a viseversa validator.
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        # Which model this serializer will work with.
        model = Registration

        # Which model fields will be shown/accepted in the API.
        fields = ['id', 'name', 'email', 'password', 'date_of_birth']



# Receive email+password
# → find the Django user
# → check password
# → create access and refresh tokens
# refresh -> a long lasting token, when access token expires, it sends token, recives new access token. 
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        User = get_user_model()
#          - validate() runs when the login data is checked.
#          - data contains the submitted email and password.
#          - get_user_model() gives us Django’s User model so we can search for the account.

        user = User.objects.filter(email=data['email']).first()
        # user is searched based on email, if email not found then return exception

        if user is None:
            raise serializers.ValidationError("Invalid email or password")

        user = authenticate(
            username=user.username,
            password=data['password']
        )

        # again checked with password. 
        if user is None:
            raise serializers.ValidationError("Invalid email or password")


        refresh = RefreshToken.for_user(user)
        # if user is valided, then for that specific user, a refresh token is generated.
        
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
