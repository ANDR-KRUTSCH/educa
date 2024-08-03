from django.http.request import HttpRequest
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from .permissions import IsEnrolled
from .pagination import StandardPagination
from .serializers import SubjectSerializer, CourseSerializer, CourseWithContentsSerializer
from ..models import Subject, Course

# class SubjectListView(generics.ListAPIView):
#     queryset = Subject.objects.annotate(total_courses=Count('courses'))
#     serializer_class = SubjectSerializer
#     pagination_class = StandardPagination


# class SubjectDetailView(generics.RetrieveAPIView):
#     queryset = Subject.objects.annotate(total_courses=Count('courses'))
#     serializer_class = SubjectSerializer


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.prefetch_related('modules')
    serializer_class = CourseSerializer
    pagination_class = StandardPagination

    @action(detail=True, methods=['post'], authentication_classes=[BasicAuthentication], permission_classes = [IsAuthenticated])
    def enroll(self, request: HttpRequest, *args, **kwargs) -> Response:
        course: Course = self.get_object()
        course.students.add(request.user)
        return Response(data=dict(enrolled=True))
    
    @action(detail=True, methods=['get'], serializer_class=CourseWithContentsSerializer, authentication_classes=[BasicAuthentication], permission_classes = [IsAuthenticated, IsEnrolled])
    def contents(self, request: HttpRequest, *args, **kwargs) -> Response:
        return self.retrieve(request=request, *args, **kwargs)


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.annotate(total_courses=Count('courses'))
    serializer_class = SubjectSerializer
    pagination_class = StandardPagination


# class CourseEnrollView(APIView):
#     authentication_classes = [BasicAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request: HttpRequest, pk: int, format: None = None):
#         course = get_object_or_404(klass=Course, pk=pk)
#         course.students.add(request.user)
#         return Response(data=dict(enrolled='ok'))