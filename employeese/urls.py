# from django.urls import path
# from . import views

# urlpatterns = [
#     # Authentication APIs
#     path('signup/', views.signup, name='signup'),
#     path('login/', views.login_user, name='login'),
#     path('logout/', views.logout_user, name='logout'),
#     path('token/refresh/', views.refresh_access_token, name='refresh_access_token'),
#     # Employee APIs
#     path('employees/', views.get_employees, name='get_employees'),
#     path('employees/<int:pk>/', views.get_employee_by_id, name='get_employee_by_id'),
#     path('employees/<int:pk>/update/', views.update_employee, name='update_employee'),
#     # path('employees/<int:pk>/delete/', views.delete_employee, name='delete_employee'),
#     path('delete-user/<int:pk>/', views.delete_user, name='delete_user'),
#     path('filter-user/', views.filter_employees, name='filter_user'),
#     path('search-user/', views.filter_employees, name='search_user'),
#     path('paginate-user/', views.filter_employees, name='paginate_user'),
#     path('sort-user/', views.filter_employees, name='sort_user'),
#     path('upload-profile/<int:pk>/', views.upload_profile_picture, name='upload-profile'),
    
#     path('signup/', views.signup_page, name='signup_page'),
#     path('login/', views.login_page, name='login_page'),
#     path('employees/', views.employee_list, name='employee_list'),
#     path('logout/', views.logout_page, name='logout_page'),
#     # path('api/', include('employeese.urls')), 
# ]


from django.urls import path
from . import views

urlpatterns = [
    # 🌐 Frontend Pages (Jinja Templates)
    path('', views.home, name='home'),
    path('signup/', views.signup_page, name='signup_page'),
    path('login/', views.login_page, name='login_page'),
    path('employees/', views.employee_list, name='employee_list'),
    path('logout/', views.logout_page, name='logout_page'),
]
