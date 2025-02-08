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

urlpatterns = [
    path("up/", include("up.urls")),
    path("", include("pages.urls")),
    path("hra_auth/", include("hra_auth.urls")),
    path("hra_tenants/", include("hra_tenants.urls")),
    path("admin/", admin.site.urls),
    path("hra_address/", include("hra_address.urls")),
    path("hra_bank_details/", include("hra_bank_details.urls")),
    path("hra_reporting_manager/", include("hra_reporting_manager.urls")),
    path("hra_education/", include("hra_education.urls")),
    path("hra_experience/", include("hra_experience.urls")),
    path("hra_customers/", include("hra_customers.urls")),
    path("hra_purchase_orders/", include("hra_purchase_orders.urls")),
    path("hra_invoices/", include("hra_invoices.urls")),
    path("hra_timesheets/", include("hra_timesheets.urls")),
    # re_path(r'^docs/', include('rest_framework_docs.urls')), // https://www.drfdocs.com/installation/
]
if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
        path("__debug__/", include("debug_toolbar.urls"))
    ]
