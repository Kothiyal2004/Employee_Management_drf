from django.urls import path
from . import views

urlpatterns = [
    # Authentication APIs
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('token/refresh/', views.refresh_access_token, name='refresh_access_token'),

    # Employee APIs
    path('employees/', views.get_employees, name='get_employees'),
    path('employees/<int:pk>/', views.get_employee_by_id, name='get_employee_by_id'),
    path('employees/<int:pk>/update/', views.update_employee, name='update_employee'),
    path('delete-user/<int:pk>/', views.delete_user, name='delete_user'),

    # Advanced Query APIs
    path('filter-user/', views.filter_employees, name='filter_user'),
    path('upload-profile/<int:pk>/', views.upload_profile_picture, name='upload_profile'),
]
