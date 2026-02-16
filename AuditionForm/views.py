from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render,HttpResponse
from rest_framework import status
from .models import AuditionData
from .serializers import AuditionDataSerializer
from .serializers import LoginSerializer
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import OTP
from twilio.rest import Client
from django.conf import settings
from .serializers import SendOtpSerializer, VerifyOtpSerializer
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
import random
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import NotFound
from django.http import Http404
import resend
import os

# def get_tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access_token),
#     } 

class AuditionDataView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = AuditionDataSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except:
                    return Response(
                        {"roll": ["This roll number already exists."]},
                        status=status.HTTP_400_BAD_REQUEST
                    )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request):
        if not request.user.is_authenticated:
            raise Http404
        
        data = AuditionData.objects.all()
        serializer = AuditionDataSerializer(data, many=True)
        return Response(serializer.data)

class RegisterUserView(APIView):  # Separate view for user registration
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request):
        data = User.objects.all()
        serializer = UserSerializer(data, many=True)
        return Response(serializer.data)

@csrf_exempt
def send_email_to_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_email = data.get('email')  # Extract email from the request
            
            if not user_email:
                return JsonResponse({'status': 'error', 'message': 'Email field is required.'})

            # Send success email to the user
            subject = "Welcome to SAE Audition - Let's Crush This Challenge! "
            message = "Congrats on moving forward to the SAE Audition! This is the college's most demanding audition, where only the best rise to the top. It's your chance to showcase your skills, creativity, and passion. \n \nPrepare to face exciting challenges that will push your limits and ignite your innovative spirit. Every task is an opportunity to shine and grow—whether it's teamwork, leadership, or technical expertise. \n \nWe know you're ready. Stay focused, bring your A-game, and make the most of every moment. \n \nLet's make this audition unforgettable. Best of luck!\n \n \n \nWarm regards, \nSAEINDIA Collegiate Club\nNIT Durgapur"
            from_email = settings.EMAIL_HOST_USER  # Use key from settings
            recipient_list = [user_email]

            send_mail(subject, message, from_email, recipient_list)
            
            return JsonResponse({'status': 'success', 'message': 'Email sent successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})



class SendOtpView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendOtpSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data['email']

            OTP.objects.filter(email=email).delete()
            otp = random.randint(100000, 999999)

            try:
                print("STEP 1: starting resend")

                api_key = os.environ.get("RESEND_API_KEY")
                print("STEP 2: API KEY EXISTS:", api_key is not None)

                resend.api_key = api_key

                response = resend.Emails.send({
                    "from": "onboarding@resend.dev",
                    "to": [email],
                    "subject": "Your OTP for Admin Login",
                    "html": f"<h2>Your OTP is {otp}</h2>"
                })

                print("STEP 3: resend response:", response)

                OTP.objects.create(otp=str(otp), email=email)

                return Response({"message": "OTP sent successfully!"}, status=200)

            except Exception as e:
                print("🔥🔥🔥 RESEND FULL ERROR:", str(e))
                return Response({"error": str(e)}, status=500)

        return Response(serializer.errors, status=400)
            
class VerifyOtpView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp_input = serializer.validated_data['otp']

            try:
                otp_record = OTP.objects.get(email=email)

                # Check if OTP is expired
                if otp_record.is_expired():
                    return Response({"message": "OTP expired. Please request a new one."}, status=status.HTTP_400_BAD_REQUEST)

                # Check if OTP matches
                if otp_record.otp == otp_input:
                    return Response({"success": True, "message": "OTP verified successfully!"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

            except OTP.DoesNotExist:
                return Response({"message": "No OTP found for this email."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        # ❗ stop immediately if invalid input
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        # authenticate using Django auth system
        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # create JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "username": user.username
        }, status=status.HTTP_200_OK)


class CustomTokenObtainView(APIView):
    permission_classes = [AllowAny]  # Allow anyone to request the token

    def post(self, request):
        # Get username and password from the request data
        username = request.data.get("username")
        password = request.data.get("password")
        
        try:
            # Attempt to authenticate the user
            user = User.objects.get(username=username)

            if user.check_password(password):
                # Create a refresh token and access token for the user
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)

                # Return both access and refresh tokens
                return Response({
                    'access': access_token,
                    'refresh': str(refresh)
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
class ValidateTokenView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure that the request is authenticated

    def get(self, request):
        """
        This view validates the JWT token provided in the request's Authorization header.
        If the token is valid, it returns a success message, otherwise returns an error.
        """
        try:
            # If the token is valid, the user will be authenticated
            return Response({"message": "Token is valid"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
class AdminDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'Welcome to the Admin Dashboard'}, status=status.HTTP_200_OK)

class DeleteObjectView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        try:
            obj = AuditionData.objects.get(pk=pk)
            obj.delete()
            return Response({"message": "Object deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except AuditionData.DoesNotExist:
            raise NotFound(detail="Object not found")

class SearchView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        Namequery = request.GET.get('Namequery', '')
        Rollquery = request.GET.get('Rollquery', '')
        Domainquery = request.GET.get('Domainquery', '')
        Genderquery = request.GET.get('Genderquery', '')
        data = AuditionData.objects.all()

        if Namequery:
            data = data.filter(name__icontains=Namequery)
        elif Rollquery:
            data = data.filter(roll__icontains=Rollquery)
        elif Domainquery:
            data = data.filter(domain__icontains=Domainquery)
        elif Genderquery:
            data = data.filter(gender__icontains=Genderquery)

        # Filter works by query and type_of_work

        
        serializer = AuditionDataSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
from rest_framework.permissions import IsAuthenticated

class ProtectedAdminView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({'message': 'You are authorized!'}, status=200)