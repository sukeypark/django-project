import datetime

from django.utils import timezone
from django.db import models

class Question(models.Model):
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField(null=True, blank=True)
    question_text = models.CharField(max_length=200)
    # --str-- is called whenever you call str() on an obj
    def __str__(self):
        return self.question_text
    '''
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    '''
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text