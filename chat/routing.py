from django.urls import re_path

from . import consumers

websocket_urlpatterns = (
    re_path(route=r'ws/chat/room/(?P<course_id>\d+)/$', view=consumers.ChatConsumer.as_asgi()),
)