import copy

from django.core.paginator import Paginator
from django.template.response import TemplateResponse
from django.shortcuts import render

QUESTIONS = [
    {
        'title': f'Title {i}',
        'id': i,
        'text': f'This is text for question № {i}',
        'tags': ["tag_" + str(i % 4), "blabla"]
    } for i in range(30)
]

ANSWERS = [f"Sometimes answer is in your knowledge, so you just have to just find it yorself {i}" for i in range(10)]

TAGS = ["tag_0", "tag_1", "tag_2", "tag_3", "blabla"]


def index(request):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(QUESTIONS, 5)
    page = paginator.page(page_num)
    return render(request, 'index.html', context={'questions': page.object_list, 'page_obj': page, 'tags': TAGS})


def hot(request):
    hot_questions = copy.deepcopy(QUESTIONS)
    hot_questions.reverse()
    return render(request, 'hot.html', context={'questions': hot_questions, 'tags': TAGS})


def login(request):
    return render(request, 'login.html', context={'tags': TAGS})


def settings(request):
    return render(request, 'settings.html', context={'tags': TAGS})


def signup(request):
    return render(request, 'signup.html', context={'tags': TAGS})


def tag(request, tag_name):
    tag_questions = [question for question in QUESTIONS if tag_name in question['tags']]
    page_num = request.GET.get('page', 1)
    paginator = Paginator(tag_questions, 5)
    page = paginator.page(page_num)
    return render(request, 'tag.html', context={'questions': page.object_list, 'page_obj': page, 'tag_name': tag_name, 'tags': TAGS})


def question(request, question_id):
    question = QUESTIONS[question_id]
    page_num = request.GET.get('page', 1)
    paginator = Paginator(ANSWERS, 3)
    page = paginator.page(page_num)
    return render(request, 'question.html', context={'question': question, 'tags': TAGS, 'answers': page.object_list, 'page_obj': page})


def ask(request):
    return render(request, 'ask.html', context={'tags': TAGS})
