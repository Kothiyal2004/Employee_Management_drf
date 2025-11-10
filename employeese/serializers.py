# from rest_framework import serializers
# from .models import Employee

# class EmployeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Employee
#         fields = ['id', 'name', 'age']

# from rest_framework import serializers
# from .models import Employee  # ✅ Corrected import

# class EmployeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Employee   # ✅ Use the correct model name
#         fields = '__all__'
from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'
        




