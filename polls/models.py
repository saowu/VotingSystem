import datetime
from typing import Any

from django.db import models

# Create your models here.
from django.utils import timezone


class Questionnaire(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title


# 问题
class Question(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200)
    is_checkbox = models.BooleanField(default=False)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def get_questionnaire_title(self):
        return self.questionnaire.title

    def get_chioce_count(self):
        return self.choice_set.count()

    def get_vote_count(self):
        _count = 0
        for choice in self.choice_set.all():
            _count += choice.votes
        return _count

    # def was_published_recently(self):
    #     now = timezone.now()
    #     return now - datetime.timedelta(days=1) <= self.pub_date <= now
    # was_published_recently.admin_order_field = 'pub_date'
    # was_published_recently.boolean = True
    get_questionnaire_title.short_description = 'questionnaire'
    get_chioce_count.short_description = 'Total chioce'
    get_vote_count.short_description = 'Total votes'


# 选择
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


# 用户
class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    occupation = models.CharField(max_length=200)
    message = models.CharField(max_length=500)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return '<%s:%s>' % (self.name, self.gender)

    def __setattr__(self, name: str, value: Any) -> None:
        super().__setattr__(name, value)
