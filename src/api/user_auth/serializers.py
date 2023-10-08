from django.core.validators import MinLengthValidator
from rest_framework import serializers
from django.contrib.auth.models import User

from src.user_auth.validators import DigitValidator, UppercaseValidator


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate_password(self, value):
        MinLengthValidator(limit_value=8)(value)  # Check minimum length
        UppercaseValidator().validate(value)  # Check for at least one uppercase letter
        DigitValidator().validate(value)  # Check for at least one digit

        return value


class LoginResponseSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def validate_password1(self, value):
        MinLengthValidator(limit_value=8)(value)  # Check minimum length
        UppercaseValidator().validate(value)  # Check for at least one uppercase letter
        DigitValidator().validate(value)  # Check for at least one digit

        return value

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError("The two password fields must match.")
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password1']
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='userprofile.avatar')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'avatar')

    def update(self, instance, validated_data):
        # Update the 'avatar' field using the 'userprofile.avatar' source
        if 'userprofile' in validated_data:
            avatar = validated_data.pop('userprofile').get('avatar')
            instance.userprofile.avatar = avatar
            instance.userprofile.save()

        # Update other fields if needed
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#
#         # Add custom claims
#         token['username'] = user.username
#         token['email'] = user.email
#         # ...
#
#         return token
#

# class UserLoginSerializer(serializers.Serializer):
#     username = serializers.CharField(required=True)
#     password = serializers.CharField(write_only=True, required=True)
#
#

# class ProfileSerializer(serializers.ModelSerializer):
#     notes = NoteSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = CustomUser
#         fields = '__all__'
