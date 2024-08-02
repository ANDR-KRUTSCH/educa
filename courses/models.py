from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from .fields import OrderField

User = get_user_model()

# Create your models here.
class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = (
            'title',
        )

    def __str__(self) -> str:
        return self.title
    

class Course(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='courses_created')
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(to=User, blank=True, related_name='courses_joined')

    class Meta:
        ordering = (
            '-created',
        )

    def __str__(self) -> str:
        return self.title
    

class Module(models.Model):
    course = models.ForeignKey(to=Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        ordering = (
            'order',
        )

    def __str__(self) -> str:
        return f'{self.order}. {self.title}'
    

class Content(models.Model):
    module = models.ForeignKey(to=Module, on_delete=models.CASCADE, related_name='contents')
    content_type = models.ForeignKey(to=ContentType, on_delete=models.CASCADE, limit_choices_to={'model__in': ('text', 'file', 'image', 'video')})
    object_pk = models.PositiveIntegerField()
    item = GenericForeignKey(ct_field='content_type', fk_field='object_pk')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = (
            'order',
        )


class ItemBase(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='%(class)s_related')
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title
    
    def render(self):
        return render_to_string(template_name=f'courses/content/{self._meta.model_name}.html', context=dict(item=self))
    

class Text(ItemBase):
    content = models.TextField()


class File(ItemBase):
    file = models.FileField(upload_to='files')


class Image(ItemBase):
    file = models.FileField(upload_to='images')


class Video(ItemBase):
    url = models.URLField()