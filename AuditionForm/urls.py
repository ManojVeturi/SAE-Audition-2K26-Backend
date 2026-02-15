
from django.urls import path, re_path
from AuditionForm import views
from django.views.generic import TemplateView
from .views import send_email_to_user
from .views import SendOtpView, VerifyOtpView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import ValidateTokenView, CustomTokenObtainView

urlpatterns = [
    # path("", views.frontpage, name='frontpage'),
    path("api/auditionform/", views.AuditionDataView.as_view(), name='Auditiondataview'),
    path("api/register/", views.RegisterUserView.as_view(), name='RegisterUserView'),
    path("api/login/", views.LoginUserView.as_view(), name='LoginUserView'),
    path("api/search/", views.SearchView.as_view(), name='SearchView'),
    path("api/delete/<int:pk>/", views.DeleteObjectView.as_view(), name='DeleteObjectView'),
    path('api/send-email-to-user/', send_email_to_user, name='send_email_to_user'),
    path('api/send-otp/', SendOtpView.as_view(), name='send_otp'),
    path('api/verify-otp/', VerifyOtpView.as_view(), name='verify_otp'),
    path('api/token/', CustomTokenObtainView.as_view(), name='custom_token_obtain'),
    path('api/validate-token/', ValidateTokenView.as_view(), name='validate_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # re_path(r'^.*$', TemplateView.as_view(template_name='react/dist/index.html'))
    # re_path(r'^.*$', TemplateView.as_view(template_name='index.html')),
    # path("api/checkroll/", views.SearchView.as_view(), name='SearchView'),
]
