from django.contrib import admin

from polls.models import Question, Choice, Poll, Answer

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Poll)
admin.site.register(Answer)
