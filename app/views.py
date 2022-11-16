from django.shortcuts import render

from . import util
from .models import Question, Answer, Profile, Tag


def index(request):
    questions = Question.objects.get_new_questions()
    context = {'questions': util.paginate(request, questions)}
    return render(request, 'index.html', context=context)


def question(request, question_id: int):
    question_item = Question.objects.get_question(question_id)
    context = {'question': question_item, 'answers': Answer.objects.filter(question=question_id)}
    return render(request, 'question.html', context=context)


def hot(request):
    questions = Question.objects.get_hot_questions()
    context = {'questions': util.paginate(request, questions)}
    return render(request, 'hot.html', context=context)


def tag(request, tag_id: int):
    tag_item = Tag.objects.get_tag(tag_id)
    questions = util.paginate(request, tag_item.questions.all())
    context = {'tag': tag_item, 'questions': questions}
    return render(request, 'tag.html', context=context)


def profile(request, profile_nickname: str):
    profile_item = Profile.objects.get_profile(profile_nickname)
    questions = util.paginate(request, profile_item.questions.all())
    context = {'profile': profile_item, 'questions': questions}
    return render(request, 'profile.html', context=context)


def login(request):
    return render(request, 'login.html')


def singup(request):
    return render(request, 'singup.html')


def settings(request):
    profile_item = Profile.objects.get_profile('root')
    context = {'profile': profile_item}
    return render(request, 'settings.html', context)


def ask(request):
    return render(request, 'ask.html')
