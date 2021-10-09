"""Create a model for polls."""
import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Create a question model."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date end',
                                    default=timezone.now() +
                                    datetime.timedelta(days=1))

    def __str__(self):
        """Use to compare with other object."""
        return self.question_text

    def was_published_recently(self):
        """Use to check was that poll published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    def was_closed(self):
        """Use to check was that poll closed."""
        now = timezone.now()
        return self.end_date <= now
    was_closed.boolean = True
    was_closed.short_description = 'Closed?'

    def is_published(self):
        """Use to check is that poll published."""
        now = timezone.now()
        return self.pub_date <= now
    is_published.boolean = True
    is_published.short_description = 'Published?'

    def can_vote(self):
        """Use to check that poll can vote."""
        now = timezone.now()
        return self.is_published() and \
            not self.was_closed() and \
            now <= self.end_date


class Choice(models.Model):
    """Create choice model."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Use to compare with other object."""
        return self.choice_text
