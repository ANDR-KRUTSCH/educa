from rest_framework.permissions import BasePermission

from django.http.request import HttpRequest

from ..models import Course

class IsEnrolled(BasePermission):
    def has_object_permission(self, request: HttpRequest, view, obj: Course):
        return obj.students.filter(pk=request.user.pk).exists()