from tkinter import Entry

from django.http import HttpResponse
from django.shortcuts import render

from . import models, util


def index(request):
    questions = models.QUESTIONS
    context = util.paginate(request, questions)
    return render(request, 'index.html', context=context)


def question(request, question_id: int):
    question_item = models.QUESTIONS[question_id]
    context = {'question': question_item, 'answers': models.ANSWERS}
    return render(request, 'question.html', context=context)


def hot(request):
    questions = sorted(models.QUESTIONS, key=lambda i: i['rating'], reverse=True)
    context = util.paginate(request, questions)
    return render(request, 'hot.html', context=context)


def tag(request, question_id: int,  tag_id: int):
    tag_item = models.QUESTIONS[question_id].tags[tag_id]
    context = {'tag': tag_item, 'questions': models.QUESTIONS}
    #return render(request, 'tag.html', context=context)
    return HttpResponse("id %s" % models.QUESTIONS[question_id].tags[tag_id])


def login(request):
    return render(request, 'login.html')


def singup(request):
    return render(request, 'singup.html')


def ask(request):
    return render(request, 'ask.html')
