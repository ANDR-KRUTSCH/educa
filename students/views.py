from typing import Any

from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy

from courses.models import Course
from .forms import CourseEnrollForm

# Create your views here.
class StudentsRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')

    def form_valid(self, form: UserCreationForm) -> HttpResponse:
        user = authenticate(request=self.request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        login(request=self.request, user=user)
        return super().form_valid(form)
    

class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form: CourseEnrollForm) -> HttpResponse:
        self.course: Course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form=form)
    
    def get_success_url(self) -> str:
        return reverse_lazy('student_course_detail', args=[self.course.pk])
    

class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(students__in=[self.request.user])
    

class StudentCourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'students/course/detail.html'

    def get_queryset(self) -> QuerySet[Any]:
        return super().get_queryset().filter(students__in=[self.request.user])
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        course: Course = self.get_object()

        if 'module_pk' in self.kwargs:
            context['module'] = course.modules.get(pk=self.kwargs['module_pk'])
        else:
            context['module'] = course.modules.first()
        
        return context