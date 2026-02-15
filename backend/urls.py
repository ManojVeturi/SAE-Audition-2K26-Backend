from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ Google auth routes (REQUIRED)
    path('accounts/', include('allauth.urls')),

    # your app routes
    path("", include("AuditionForm.urls")),
]
