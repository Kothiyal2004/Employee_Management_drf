# """
# URL configuration for employee_api project.

# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/5.2/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """

# from django.contrib import admin
# from django.urls import path, include
# from django.shortcuts import render
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi
# from employeese.views import home
# from rest_framework import permissions


# schema_view = get_schema_view(
#     openapi.Info(
#         title="Employee Management API",
#         default_version='v1',
#         description="API for managing employees, authentication, and profiles.",
#         contact=openapi.Contact(email="admin@example.com"),
#         license=openapi.License(name="MIT License"),
#     ),
#     public=True,
#     permission_classes=(permissions.AllowAny,),
# )



# urlpatterns = [
#     path('', home),  # root /
#     path('admin/', admin.site.urls),
#     path('api/', include('employeese.urls')),  # API routes
#     path('api/', include('employeese.api_urls')),  # DRF endpoints (optional)
#     path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
#     # ReDoc (drf-yasg also supports redoc UI)
#     path('swagger/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#     # path('signup/', views.signup_page, name='signup_page'),
#     # path('login/', views.login_page, name='login_page'),
#     # path('employees/', views.employee_list, name='employee_list'),
    
# ]

from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Swagger / Redoc Documentation Setup
schema_view = get_schema_view(
    openapi.Info(
        title="Employee Management API",
        default_version='v1',
        description="API for managing employees, authentication, and profiles.",
        contact=openapi.Contact(email="admin@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ Frontend UI Routes (Jinja2 templates)
    path('', include('employeese.urls')),

    # ✅ Backend API Routes (pure JSON API)
    path('api/', include('employeese.api_urls')),

    # ✅ Swagger / Redoc Docs
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]



