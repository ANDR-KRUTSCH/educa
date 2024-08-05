from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .models import Course

def subdomain_course_middleware(get_response):
    def middleware(request: HttpRequest) -> HttpResponseRedirect:
        host_parts = request.get_host().split('.')
        
        if len(host_parts) > 2 and host_parts[0] != 'www':
            course = get_object_or_404(klass=Course, slug=host_parts[0])
            course_url = reverse(viewname='course_detail', args=[course.slug])

            url = '{}://{}{}'.format(request.scheme, '.'.join(host_parts[1:]), course_url)

            return redirect(to=url)
        
        return get_response(request)
    
    return middleware