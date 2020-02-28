from django.contrib import admin

# Register your models here.
from .models import Question, Choice, User, Questionnaire


# StackedInline
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    search_fields = ['questionnaire__title']
    list_filter = ['pub_date', 'is_checkbox']
    list_display = ('get_questionnaire_title', 'question_text', 'is_checkbox', 'pub_date', 'get_chioce_count', 'get_vote_count')
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]

    def has_add_permission(self, request):
        return False


class QuestionnaireAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_filter = ['pub_date']
    list_display = ('title', 'pub_date')
    fieldsets = [
        (None, {'fields': ['title']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [QuestionInline]


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'occupation', 'email', 'message', 'pub_date')


admin.site.register(Question, QuestionAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
