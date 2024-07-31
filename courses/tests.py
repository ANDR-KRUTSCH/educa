from django.test import TestCase
from django.contrib.auth.models import User

from .models import Subject, Course, Module

# Create your tests here.
class OrderFieldTest(TestCase):
    
    def test(self) -> None:
        user = User(username='user')
        user.set_password(raw_password='password')
        user.save()

        subject = Subject.objects.create(title='Programming', slug='programming')
        
        course_1 = Course.objects.create(owner=user, subject=subject, title='Django', slug='django', overview='Introduction to Django')
        course_2 = Course.objects.create(owner=user, subject=subject, title='FastAPI', slug='fastapi', overview='Introduction to FastAPI')        

        module_1 = Module.objects.create(course=course_1, title='Installing')
        module_2 = Module.objects.create(course=course_1, title='Project')
        module_3 = Module.objects.create(course=course_1, title='App')
        module_4 = Module.objects.create(course=course_1, title='Models')
        module_5 = Module.objects.create(course=course_1, title='Views')
        module_6 = Module.objects.create(course=course_1, title='URLs')
        module_7 = Module.objects.create(course=course_1, title='Templates')

        module_8 = Module.objects.create(course=course_2, title='Installing')
        module_9 = Module.objects.create(course=course_2, title='Running Server')
        module_10 = Module.objects.create(course=course_2, title='Endpoints Defining')

        self.assertEqual([module_1.order, module_2.order, module_3.order, module_4.order, module_5.order, module_6.order, module_7.order], [i for i in range(7)])
        self.assertEqual([module_8.order, module_9.order, module_10.order], [i for i in range(3)])