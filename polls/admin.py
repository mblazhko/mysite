from django.contrib import admin

from polls.models import Question, Choice, Poll, Answer


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fields = ["question_text", "poll"]
    list_display = ["question_text", "poll"]
    inlines = [ChoiceInline]


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 2


class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["poll_name", "poll_description", "owner"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    list_display = ["poll_name", "pub_date", "owner"]
    list_filter = ["owner", "pub_date"]
    inlines = [QuestionInline]


class AnswerAdmin(admin.ModelAdmin):
    list_display = ["choice", "owner"]
    list_filter = ["owner"]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Poll, PollAdmin)
admin.site.register(Answer, AnswerAdmin)
