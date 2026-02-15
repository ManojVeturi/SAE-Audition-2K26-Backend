from rest_framework import serializers
from .models import AuditionData
from django.contrib.auth.models import User
from .models import OTP

class AuditionDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = AuditionData
        fields = '__all__'

    def validate_roll(self, value):
        if AuditionData.objects.filter(roll=value).exists():
            raise serializers.ValidationError("This roll number already exists.")
        return value


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(write_only=True)  # Ensure password is not exposed

    def validate(self, data):
        # You can add custom validation logic here (e.g., validate password length)
        return data
class SendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        # Check if OTP exists for this email
        try:
            otp_instance = OTP.objects.get(email=email, otp=otp)
            def is_expired(self):
                """Check if OTP is expired (valid for 5 minutes)"""
                return timezone.now() > self.created_at + timedelta(minutes=5)

            # Check if OTP is expired
            if otp_instance.is_expired():
                raise serializers.ValidationError("OTP has expired.")
        
        except OTP.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP.")

        return data