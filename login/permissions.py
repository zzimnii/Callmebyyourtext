from rest_framework import permissions

class CustomReadOnly(permissions.BasePermission):
    # GET => allowany 
    # PUT/PATCH => allowed User
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS: # SAFE_METHODS => 데이터 변동없는 method
            return True
        return obj.user == request.user