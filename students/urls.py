from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = (
    path(route='register/', view=views.StudentsRegistrationView.as_view(), name='student_registration'),
    path(route='enroll-course/', view=views.StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    path(route='courses/', view=views.StudentCourseListView.as_view(), name='student_course_list'),
    path(route='course/<pk>/', view=cache_page(timeout=60 * 15)(views.StudentCourseDetailView.as_view()), name='student_course_detail'),
    path(route='course/<pk>/<module_pk>/', view=cache_page(views.StudentCourseDetailView.as_view()), name='student_course_detail_module'),
)