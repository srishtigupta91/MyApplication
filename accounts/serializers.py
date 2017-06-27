from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_decode
from rest_framework import exceptions
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from accounts import messages
from accounts.models import User

class UserSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id','name','screen_name', 'dob','gender',"role",)


class RegistrationSerializers(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("id","name", "email", "password", "role",)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class RegistrationConfirmationSerializer(serializers.Serializer):
        uid = serializers.CharField()
        token = serializers.CharField()

        default_error_messages = {
            'invalid_token': messages.INVALID_TOKEN_ERROR,
            'invalid_uid': messages.INVALID_UID_ERROR,
        }

        def validate_uid(self, value):
            try:
                uid = urlsafe_base64_decode(value)
                self.user = User.objects.get(pk=uid)
            except (User.DoesNotExist, ValueError,
                    TypeError, OverflowError) as error:
                raise serializers.ValidationError(
                    self.error_messages['invalid_uid'])
            return value

        def validate(self, attrs):
            attrs = super(RegistrationConfirmationSerializer, self).validate(attrs)
            if not self.context['view'].token_generator.check_token(
                    self.user, attrs['token']):
                raise serializers.ValidationError(
                    self.error_messages['invalid_token'])
            return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        required=False,
        min_length=4,
        style={'input_type': 'password'})


    default_error_messages = {
        'inactive_account': messages.INACTIVE_ACCOUNT_ERROR,
        'invalid_credentials': messages.INVALID_CREDENTIALS_ERROR,
    }

    def __init__(self, *args, **kwargs):
        super(LoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
        except:
            raise exceptions.ValidationError("user not found")
        if not user.is_active:
            raise exceptions.ValidationError("User is inactive state")
        self.user = authenticate(
            username=attrs.get(User.USERNAME_FIELD),
            password=attrs.get('password'))

        if not self.user:
             raise serializers.ValidationError(
                 self.error_messages['invalid_credentials'])
        return attrs


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source='key')
    is_profile_complete = serializers.SerializerMethodField()

    def get_is_profile_complete(self, obj):
        if obj.user.screen_name and obj.user.draw_location:
            return True
        else:
            return False

    class Meta:
        model = Token
        fields = (
            'auth_token','is_profile_complete',
        )
