from rest_framework.permissions import BasePermission, SAFE_METHODS

class EmployeePermission(BasePermission):
    def has_object_permission(self, request, view):
        print("Inside has_object_permission", view)

        user = request.user
    
        if not user or not user.is_authenticated:
            return False
        
        if user and user==view:
            return True

        # ✅ Admin can do anything
        if user.is_staff:
            return True

        # ✅ HR can only read (GET, HEAD, OPTIONS)
        if user.groups.filter(name='HR').exists():
            return request.method in SAFE_METHODS

        # 🚫 Others cannot access employee list
        return False
    
    def picture_permission(self, request, view):
        user = request.user # logged in user 
        #view.user # employee fetched from DB 
        if user != view.user and  user.is_staff == False:
            return False
        return True

