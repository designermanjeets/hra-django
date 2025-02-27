"""
URL configuration for hello project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import include
from django.urls import path, re_path

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication


schema_view = get_schema_view(
   openapi.Info(
      title="HRK API",
      default_version="v1",
      description="HRK Ai System API",
      terms_of_service="https://aiinfox.com/terms-and-conditions/",
      contact=openapi.Contact(email="info@aiinfox.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(AllowAny,),

)



urlpatterns = [
    # path("up/", include("up.urls")),
    path("", include("pages.urls")),
    path("auth/", include("hra_auth.urls")),
    path('users/', include('hra_users.urls')),
    path("tenants/", include("hra_tenants.urls")),
    path("admin/", admin.site.urls),
    path("address/", include("hra_address.urls")),
    path("bank_details/", include("hra_bank_details.urls")),
    path("reporting_manager/", include("hra_reporting_manager.urls")),
    path("education/", include("hra_education.urls")),
    path("experience/", include("hra_experience.urls")),
    path("customers/", include("hra_customers.urls")),
    path("purchase_orders/", include("hra_purchase_orders.urls")),
    path("invoices/", include("hra_invoices.urls")),
    path("timesheets/", include("hra_timesheets.urls")),
    path("global_configs/", include("hra_global_configs.urls")),
    path("lookup/", include("hra_lookup.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
        path("__debug__/", include("debug_toolbar.urls"))
    ]
