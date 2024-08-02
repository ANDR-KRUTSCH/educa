from django.urls import path

from . import views

urlpatterns = (
    path(route='mine/', view=views.ManageCourseListView.as_view(), name='manage_course_list'),
    path(route='create/', view=views.CourseCreateView.as_view(), name='course_create'),
    path(route='<pk>/edit/', view=views.CourseUpdateView.as_view(), name='course_edit'),
    path(route='<pk>/delete/', view=views.CourseDeleteView.as_view(), name='course_delete'),
    path(route='<pk>/module/', view=views.CourseModuleUpdateView.as_view(), name='course_module_update'),
    path(route='module/order/', view=views.ModuleOrderView.as_view(), name='module_order'),
    path(route='content/order/', view=views.ContentOrderView.as_view(), name='content_order'),
    path(route='module/<int:module_pk>/', view=views.ModuleContentListView.as_view(), name='module_content_list'),
    path(route='module/<int:module_pk>/content/<model_name>/create/', view=views.ContentCreateUpdateView.as_view(), name='module_content_create'),
    path(route='module/<int:module_pk>/content/<model_name>/<pk>/', view=views.ContentCreateUpdateView.as_view(), name='module_content_update'),
    path(route='content/<pk>/delete/', view=views.ContentDeleteView.as_view(), name='module_content_delete'),
)