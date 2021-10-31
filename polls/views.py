"""Views for polls app."""
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Choice, Question, Vote
from django.shortcuts import redirect, get_object_or_404, render
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


class IndexView(generic.ListView):
    """Manage view for index page."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions.

        (not including those set to be published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    """Manage view for index page."""

    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """Excludes any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """Manage result view in result page."""

    model = Question
    template_name = 'polls/results.html'


@login_required()
def vote(request, question_id):
    """Make user to vote polls."""
    user = request.user
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        Vote.objects.update_or_create(user=user, defaults={'choice': selected_choice})
        for choice in question.choice_set.all():
            choice.votes = Vote.objects.filter(choice=choice).count()
            choice.save()
        if Vote.objects.filter(choice=choice).count() == 0:
            selected_choice.votes += 1
            selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results',
                                            args=(question.id,)))


def get_queryset(self):
    """
    Return the last five published questions.

    (not including those set to be published in the future).
    """
    return Question.objects.filter(
        pub_date__lte=timezone.now()
    ).order_by('-pub_date')[:5]


def detail(request, question_id):
    """View for detail page from question_id."""
    question = get_object_or_404(Question, pk=question_id)
    if question.can_vote():
        return render(request, 'polls/detail.html', {'question': question})
    else:
        messages.error(request,
                       f'Sorry, voting for Question {question_id} is not allowed')
        return redirect('polls:index')


def results(request, question_id):
    """View for result page from question_id."""
    question = get_object_or_404(Question, pk=question_id)
    if question.is_published():
        return render(request, 'polls/results.html', {'question': question})
    else:
        messages.error(request,
                       f'Sorry, Question {question_id} not published yet')
        return redirect('polls:index')

