from django.http import HttpRequest, HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from courses.models import Course

# Create your views here.
@login_required
def course_chat_room(request: HttpRequest, course_pk: int) -> HttpResponse | HttpResponseForbidden | HttpResponseRedirect:
    try:
        course = request.user.courses_joined.get(pk=course_pk)
    except Course.DoesNotExist:
        return HttpResponseForbidden()
    
    latest_messages = course.chat_messages.select_related('user').order_by('-id')[:5]
    latest_messages = reversed(latest_messages)
    
    context = dict(
        course=course,
        latest_messages=latest_messages,
    )

    return render(request=request, template_name='chat/room.html', context=context) 