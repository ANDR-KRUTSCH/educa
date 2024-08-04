from django.db import models
from django.contrib.auth import get_user_model

from courses.models import Course

User = get_user_model()

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='chat_messages')
    course = models.ForeignKey(to=Course, on_delete=models.PROTECT, related_name='chat_messages')
    content = models.TextField()
    sent_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user} on {self.course} as {self.sent_on}'