from django.urls import path, include

from rest_framework import routers

from . import views

app_name = 'courses'

router = routers.DefaultRouter()

router.register(prefix='courses', viewset=views.CourseViewSet)
router.register(prefix='subjects', viewset=views.SubjectViewSet)

urlpatterns = (
    path(route='', view=include(arg=router.urls)),
    # path(route='courses/<pk>/enroll/', view=views.CourseEnrollView.as_view(), name='course_enroll'),
    # path(route='subjects/', view=views.SubjectListView.as_view(), name='subject_list'),
    # path(route='subjects/<pk>/', view=views.SubjectDetailView.as_view(), name='subject_detail'),
)