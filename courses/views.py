from typing import Any

from braces.views import CsrfExemptMixin, JSONRequestResponseMixin

from django.db.models import Model
from django.db.models.query import QuerySet
from django.db.models.aggregates import Count
from django.forms import Form, ModelForm
from django.forms.models import modelform_factory
from django.http import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.apps import apps
from django.core.cache import cache

from students.forms import CourseEnrollForm
from .models import Subject, Course, Module, Content
from .forms import ModuleFormSet

# Create your views here.
class OwnerMixin:
    def get_queryset(self) -> QuerySet[Any]:
        qs: QuerySet = super().get_queryset()
        return qs.filter(owner=self.request.user)
    

class OwnerEditMixin:
    def form_valid(self, form: Form | ModelForm) -> Any:
        form.instance.owner = self.request.user
        return super().form_valid(form)
    

class OwnerCourseMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    model = Course
    fields = ('subject', 'title', 'slug', 'overview')
    success_url = reverse_lazy('manage_course_list')


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/manage/course/form.html'


class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/manage/course/list.html'
    permission_required = 'courses.view_course'


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    permission_required = 'courses.add_course'


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    permission_required = 'courses.change_course'


class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/manage/course/delete.html'
    permission_required = 'courses.delete_course'


class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/course/formset.html'
    course = None

    def get_formset(self, data=None):
        return ModuleFormSet(instance=self.course, data=data)
    
    def dispatch(self, request: HttpRequest, pk: int, *args: Any, **kwargs: Any) -> HttpResponse:
        self.course = get_object_or_404(klass=Course, pk=pk, owner=request.user)
        return super().dispatch(request, pk, *args, **kwargs)
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        formset = self.get_formset()

        context = dict(
            course=self.course,
            formset=formset,
        )

        return self.render_to_response(context=context)
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        formset = self.get_formset(data=request.POST)

        if formset.is_valid():
            formset.save()

            return redirect(to='manage_course_list')
        
        context = dict(
            course=self.course,
            formset=formset,
        )
        
        return self.render_to_response(context=context)
    

class ContentCreateUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/manage/content/form.html'
    module = None
    model = None
    obj = None
    
    def get_model(self, model_name: str) -> Model:
        if model_name in ['text', 'video', 'image', 'file']:
            return apps.get_model(app_label='courses', model_name=model_name)
        return None
    
    def get_form(self, model, *args: Any, **kwargs: Any) -> ModelForm:
        Form = modelform_factory(model=model, exclude=['owner', 'order', 'created', 'updated'])
        return Form(*args, **kwargs)
    
    def dispatch(self, request: HttpRequest, module_pk: int, model_name: str, pk=None, *args: Any, **kwargs: Any) -> HttpResponse:
        self.module = get_object_or_404(klass=Module, pk=module_pk, course__owner=request.user)
        self.model = self.get_model(model_name=model_name)
        if pk:
            self.obj = get_object_or_404(klass=self.model, pk=pk, owner=request.user)
        return super().dispatch(request, module_pk, model_name, pk, *args, **kwargs)
    
    def get(self, request: HttpRequest, module_pk: int, model_name: str, pk: int = None) -> HttpResponse:
        form = self.get_form(model=self.model, instance=self.obj)

        context = dict(
            form=form,
            object=self.obj,
        )

        return self.render_to_response(context=context)
    
    def post(self, request: HttpRequest, module_pk: int, model_name: str, pk: int = None) -> HttpResponse:
        form = self.get_form(model=self.model, instance=self.obj, data=request.POST, files=request.FILES)

        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()

            if not pk:
                Content.objects.create(module=self.module, item=obj)

            return redirect('module_content_list', self.module.pk)
        
        context = dict(
            form=form,
            object=self.obj,
        )

        return self.render_to_response(context=context)
    

class ContentDeleteView(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        content = get_object_or_404(klass=Content, pk=pk, module__course__owner=request.user)
        module = content.module
        content.item.delete()
        content.delete()
        return redirect('module_content_list', module.pk)
    

class ModuleContentListView(TemplateResponseMixin, View):
    template_name = 'courses/manage/module/content_list.html'
    
    def get(self, request: HttpRequest, module_pk: int, *args: Any, **kwargs: Any) -> HttpResponse:
        module = get_object_or_404(klass=Module, pk=module_pk, course__owner=request.user)

        context = dict(
            module=module,
        )

        return self.render_to_response(context=context)


class ModuleOrderView(CsrfExemptMixin, JSONRequestResponseMixin, View):
    def post(self, request: HttpRequest) -> HttpResponse:
        for pk, order in self.request_json.items():
            Module.objects.filter(pk=pk, course__owner=request.user).update(order=order)
            return self.render_json_response({'saved': 'ok'})
        

class ContentOrderView(CsrfExemptMixin, JSONRequestResponseMixin, View):
    def post(self, request: HttpRequest) -> HttpResponse:
        for pk, order in self.request_json.items():
            Content.objects.filter(pk=pk, module__course__owner=request.user).update(order=order)
            return self.render_json_response({'saved': 'ok'})
        

class CourseListView(TemplateResponseMixin, View):
    model = Course
    template_name = 'courses/course/list.html'

    def get(self, request: HttpRequest, subject: str = None) -> HttpResponse:
        subjects = cache.get(key='subjects')
        if not subjects:
            subjects = Subject.objects.annotate(total_courses=Count('courses'))
            cache.set(key='subjects', value=subjects)

        all_courses = Course.objects.annotate(total_modules=Count('modules'))

        if subject:
            subject: Subject = get_object_or_404(klass=Subject, slug=subject)
            key = f'subject_{subject.pk}_courses'
            courses = cache.get(key=key)
            if not courses:
                courses = all_courses.filter(subject=subject)
                cache.set(key=key, value=courses)
        else:
            courses = cache.get(key='all_courses')
            if not courses:
                courses = all_courses
                cache.set(key='all_courses', value=courses)

        context = dict(
            subjects=subjects,
            subject=subject,
            courses=courses,
        )

        return self.render_to_response(context=context)
    

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course/detail.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context['enroll_form'] = CourseEnrollForm(initial=dict(course=self.object))

        return context