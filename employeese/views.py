from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Employee
from .serializers import EmployeeSerializer
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Employee
from .serializers import EmployeeSerializer
from .permissions import EmployeePermission
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from django.contrib.auth.models import User
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render, redirect
from django.contrib import messages
import requests


# Change this URL if your API runs on a different port
API_BASE_URL = "http://127.0.0.1:8000/api/"


# Fetch all employees
@api_view(['GET'])
@permission_classes([IsAuthenticated, EmployeePermission])
def get_employees(request):
    # if request.user.is_staff:
    # Manually enforce object-level permission (important for FBVs)
    #   dummy employee for permission check
    employee = request.user  # dummy instance for permission check
    perm = EmployeePermission()
    if not perm.has_object_permission(request=request, view=employee):
        return Response({"error": "You do not have permission to update this employee."},
                        status=status.HTTP_403_FORBIDDEN)
    employees = Employee.objects.all()
    serializer = EmployeeSerializer(employees, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='post',
    operation_summary="Register a new employee user",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password', 'name', 'age', 'department', 'salary'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING, description='Unique username'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Employee name'),
            'age': openapi.Schema(type=openapi.TYPE_INTEGER, description='Employee age (>=18)'),
            'department': openapi.Schema(type=openapi.TYPE_STRING, description='Department'),
            'salary': openapi.Schema(type=openapi.TYPE_NUMBER, description='Salary'),
        }
    ),
    responses={201: "User created successfully", 400: "Validation error"}
)
@api_view(['POST'])
def signup(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response({"error": "Username and password are required."},
                        status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({"error": "Username already exists."},
                        status=status.HTTP_400_BAD_REQUEST)
    
    # Use a transaction so both user and employee are created together
    with transaction.atomic():
        user = User.objects.create_user(username=username, password=password)

        employee_data = {
            "user": user.id,
            "name": request.data.get("name"),
            "age": request.data.get("age"),
            "department": request.data.get("department"),
            "salary": request.data.get("salary")
        }

        serializer = EmployeeSerializer(data=employee_data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(
                {"message": f"User '{username}' and Employee '{serializer.data['name']}' created successfully"},
                status=status.HTTP_201_CREATED
            )
        else:
            # If validation fails, rollback the user creation
            user.delete()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    operation_summary="Login user and return JWT tokens",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['username', 'password'],
        properties={
            'username': openapi.Schema(type=openapi.TYPE_STRING),
            'password': openapi.Schema(type=openapi.TYPE_STRING),
        }
    ),
    responses={200: "JWT tokens returned", 401: "Invalid credentials"}
)
@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        # Log in the user (session-based, optional)
        # login(request, user)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
            },
            'access_token': access_token,
            'refresh_token': refresh_token
        }, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logout successful'}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({'error': 'Invalid token or already blacklisted'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def refresh_access_token(request):
    """
    Refresh the access token using a valid refresh token.
    """
    refresh_token = request.data.get("refresh_token")

    if not refresh_token:
        return Response(
            {"error": "Refresh token is required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        refresh = RefreshToken(refresh_token)
        new_access_token = str(refresh.access_token)

        return Response({
            "access_token": new_access_token
        }, status=status.HTTP_200_OK)

    except TokenError as e:
        return Response({
            "error": "Invalid or expired refresh token."
        }, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_employee(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = EmployeeSerializer(employee, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Employee updated successfully", "data": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, EmployeePermission])
def delete_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
        perm = EmployeePermission()
        if not perm.has_object_permission(request=request, view=user):
            return Response({"error": "You do not have permission to update this employee."},
                            status=status.HTTP_403_FORBIDDEN)
        
        user.delete()  # This automatically deletes the related Employee
        return Response(
            {"message": "User and related employee deleted successfully"},
            status=status.HTTP_200_OK
        )
    except User.DoesNotExist:
        return Response(
            {"error": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated, EmployeePermission])
def get_employee_by_id(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
    
    # Manually enforce object-level permission (important for FBVs)
    perm = EmployeePermission()
    if not perm.has_object_permission(request=request, view=employee):
        return Response({"error": "You do not have permission to view this employee."},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = EmployeeSerializer(employee)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated, EmployeePermission])
def update_employee(request, pk):


    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)

# Manually enforce object-level permission (important for FBVs)
    perm = EmployeePermission()
    if not perm.has_object_permission(request=request, view=employee):
        return Response({"error": "You do not have permission to update this employee."},
                        status=status.HTTP_403_FORBIDDEN)

    serializer = EmployeeSerializer(employee, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Employee updated successfully", "data": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    operation_summary="Filter, search, sort, and paginate employee records",
    manual_parameters=[
        openapi.Parameter('department', openapi.IN_QUERY, description="Filter by department", type=openapi.TYPE_STRING),
        openapi.Parameter('age', openapi.IN_QUERY, description="Filter by age", type=openapi.TYPE_INTEGER),
        openapi.Parameter('search', openapi.IN_QUERY, description="Search by name or department", type=openapi.TYPE_STRING),
        openapi.Parameter('ordering', openapi.IN_QUERY, description="Sort results (e.g. salary or -salary)", type=openapi.TYPE_STRING),
        openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
        openapi.Parameter('page_size', openapi.IN_QUERY, description="Number of results per page", type=openapi.TYPE_INTEGER),
    ],
    responses={200: EmployeeSerializer(many=True)}
)
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def filter_employees(request):

    # ✅ Base queryset
    employees = Employee.objects.all()

    # -------------------------
    # 1️⃣ FILTERING (e.g. ?department=IT&age=25)
    # -------------------------
    department = request.GET.get('department')
    age = request.GET.get('age')
    

    if department:
        employees = employees.filter(department__iexact=department)
    if age:
        employees = employees.filter(age=age)

    # -------------------------
    # 2️⃣ SEARCHING (e.g. ?search=john)
    # -------------------------
    search = request.GET.get('search')
    if search:
        employees = employees.filter(
            Q(name__icontains=search) |
            Q(department__icontains=search)
        )

    # -------------------------
    # 3️⃣ SORTING (e.g. ?ordering=salary or ?ordering=-salary)
    # -------------------------
    ordering = request.GET.get('ordering')
    if ordering:
        employees = employees.order_by(ordering)

    # -------------------------
    # 4️⃣ PAGINATION (?page=2&page_size=5)
    # -------------------------
    paginator = PageNumberPagination()
    paginator.page_size_query_param = 'page_size'  # user can control ?page_size=
    paginated_employees = paginator.paginate_queryset(employees, request)
    serializer = EmployeeSerializer(paginated_employees, many=True)
    return paginator.get_paginated_response(serializer.data)

@swagger_auto_schema(
    method='post',
    operation_summary="Upload profile picture for employee",
    manual_parameters=[
        openapi.Parameter('pk', openapi.IN_PATH, description="Employee ID", type=openapi.TYPE_INTEGER),
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'profile_picture': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_BINARY, description='Upload image file'),
        },
    ),
    responses={200: "Profile picture uploaded", 400: "Invalid request", 403: "No permission"}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])    #only logged in user can upload profile picture 
def upload_profile_picture(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
    perm = EmployeePermission()
    if perm.picture_permission(request=request, view=employee)==False:
        return Response({"error": "You do not have permission to update this employee profile picture."},
                        status=status.HTTP_403_FORBIDDEN)

    if 'profile_picture' not in request.FILES:
        return Response({"error": "No image uploaded."}, status=status.HTTP_400_BAD_REQUEST)

    # Save the uploaded file
    employee.profile_picture = request.FILES['profile_picture']
    employee.save()

    serializer = EmployeeSerializer(employee)
    return Response({"message": "Profile picture uploaded successfully", "data": serializer.data},
                    status=status.HTTP_200_OK)
# Optional: Root view
def home(request):
    return render(request,"employeese/signup.html",{"message": "Welcome to Employee API"})


# Frontend Views using Django Templates


# 🧾 Signup Page
def signup_page(request):
    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
            "name": request.POST.get("name"),
            "age": request.POST.get("age"),
            "department": request.POST.get("department"),
            "salary": request.POST.get("salary"),
        }
        response = requests.post(f"{API_BASE_URL}signup/", data=data)
        if response.status_code == 201:
            messages.success(request, "Signup successful! Please login.")
            return redirect("login_page")
        else:
            messages.error(request, response.json())
    return render(request, "employeese/signup.html")


# 🔑 Login Page
def login_page(request):
    if request.method == "POST":
        data = {
            "username": request.POST.get("username"),
            "password": request.POST.get("password"),
        }
        response = requests.post(f"{API_BASE_URL}login/", data=data)
        if response.status_code == 200:
            tokens = response.json()
            request.session["access_token"] = tokens["access_token"]
            request.session["username"] = tokens["user"]["username"]
            return redirect("employee_list")
        else:
            messages.error(request, "Invalid credentials")
    return render(request, "employeese/login.html")


# 👥 Employee List Page
def employee_list(request):
    token = request.session.get("access_token")
    if not token:
        return redirect("login_page")

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{API_BASE_URL}employees/", headers=headers)

    if response.status_code == 200:
        employees = response.json()
        return render(request, "employeese/employee_list.html", {"employees": employees})
    elif response.status_code == 401:
        messages.error(request, "Session expired. Please login again.")
        return redirect("login_page")
    else:
        messages.error(request, "Failed to fetch employee data.")
        return redirect("login_page")


# 🚪 Logout
def logout_page(request):
    request.session.flush()
    return redirect("login_page")
