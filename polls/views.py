from django.shortcuts import render, get_object_or_404

# Create your views here.


from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Question, Choice, User, Questionnaire


def index(request):
    all_entries = Questionnaire.objects.all()
    context = {
        'questionnaires': all_entries,
    }
    return render(request, 'polls/index.html', context)


def get_questionnaire(request, questionnaire_id):
    questionnaire = get_object_or_404(Questionnaire, pk=questionnaire_id)
    questions = questionnaire.question_set.all()
    latest_question_list = questions.order_by('is_checkbox')[:]
    context = {
        'latest_question_list': latest_question_list,
        'title': questionnaire.title,
        'count': latest_question_list.count(),
    }
    return render(request, 'polls/questions.html', context)


def submit_vote(request):
    values = request.POST.items()
    q = User(pub_date=timezone.now())
    for k, v in values:
        if len(k) > 9 and k[:8] == 'question' and k[-2:] != '[]':
            question = get_object_or_404(Question, pk=int(k[9:]))
            try:
                selected_choice = question.choice_set.get(pk=int(v))
            except (KeyError, Choice.DoesNotExist):
                print("找不到")
            else:
                selected_choice.votes += 1
                selected_choice.save()
        elif len(k) > 9 and k[:8] == 'question' and k[-2:] == '[]':
            list = request.POST.getlist(k)
            question = get_object_or_404(Question, pk=int(k[9:11]))
            for value in list:
                try:
                    selected_choice = question.choice_set.get(pk=int(value))
                except (KeyError, Choice.DoesNotExist):
                    print("找不到")
                else:
                    selected_choice.votes += 1
                    selected_choice.save()
        else:
            q.__setattr__(k, v)
    q.save()
    return HttpResponseRedirect(reverse('polls:index'))


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})


def vote(request, question_id):
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
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

# class IndexView(generic.ListView):
#     template_name = 'polls/index1.html'
#     context_object_name = 'latest_question_list'
#
#     def get_queryset(self):
#         """Return the last five published questions."""
#         return Question.objects.filter(
#             pub_date__lte=timezone.now()
#         ).order_by('-pub_date')[:5]
#
#
# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'polls/detail.html'
#
#     def get_queryset(self):
#         """
#         Excludes any questions that aren't published yet.
#         """
#         return Question.objects.filter(pub_date__lte=timezone.now())
#
#
# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'polls/results.html'
