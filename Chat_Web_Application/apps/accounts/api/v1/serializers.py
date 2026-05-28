from rest_framework import serializers
from django.contrib.auth.password_validation import (validate_password,get_password_validators,MinimumLengthValidator)
from django.conf import settings
from apps.accounts.models import User
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
import re
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

def validate_password_min8_with_special(password, user=None):
    if len(password) < 8:
        raise serializers.ValidationError("Password must be at least 8 characters long.")
    if not re.search(r"[^A-Za-z0-9]", password):
        raise serializers.ValidationError("Password must include at least 1 special character.")

    default_validators = get_password_validators(settings.AUTH_PASSWORD_VALIDATORS)
    validators_without_min_length = [validator for validator in default_validators
        if not isinstance(validator, MinimumLengthValidator)]

    try:
        validate_password(password, user, validators_without_min_length)
    except DjangoValidationError as exc:
        raise serializers.ValidationError(list(exc.messages))


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password_min8_with_special])
    password2 = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True, validators=[RegexValidator(
        regex=r'^[\w\.-]+@[\w\.-]+\.\w+$',
        message="Enter a valid email address."
    )])
    phone_number = serializers.CharField(required=False, validators=[
        MinLengthValidator(10, message="Phone number must be at least 10 digits long."),
        RegexValidator(r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    ])
    

    class Meta:
        model = User
        fields = ["email", "username", "password","password2", "phone_number"]
    
    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError("User with this email already exists.")
        return email

    # Phone validation
    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("User with this phone number already exists.")
        return value
    
    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password2": "Password and confirm password do not match"})
        return attrs

    def create(self, validated_data):
        # Remove password2 from validated_data
        validated_data.pop("password2", None)
        user = User.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"],
            phone_number=validated_data.get("phone_number")
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email","").lower().strip()   
        password = attrs.get("password")

        user = authenticate(request=self.context.get("request"), username=email, password=password)
        if not user:
            raise serializers.ValidationError("Invalid email or password")
        elif password and not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")
        elif not user.check_password(password):
            raise serializers.ValidationError("Invalid email or password")
        elif not user.is_active:
            raise serializers.ValidationError("User account is disabled")
        refresh = RefreshToken.for_user(user)
        return {
            "user": user,
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }    
        
class CommonUserResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    email = serializers.EmailField(max_length=255)
    role = serializers.CharField(max_length=255)
        
class LoginResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()
    user = CommonUserResponseSerializer()
