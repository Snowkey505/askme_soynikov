from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404, render
from app.models import Question, Answer, Tag, Profile
from django.db.models import Count


def paginate(obj_list, req, per_page=4):
    paginator = Paginator(obj_list, per_page)
    page_number = req.GET.get('page', 1)
    try:
        return paginator.get_page(page_number)
    except PageNotAnInteger:
        return paginator.get_page(1)
    except EmptyPage:
        return paginator.get_page(paginator.num_pages)


def index(req):
    paginated_cards = paginate(Question.objects.new(), req, 4)
    profile = get_object_or_404(Profile, user_id=req.user.id) if req.user.is_authenticated else None
    return render(req, 'index.html', context={
        'username': req.user.username if req.user.is_authenticated else None,
        'userpic': profile.avatar.url if profile and profile.avatar else None,
        'members': Profile.objects.best(),
        'tags': Tag.objects.popular().values_list('name', flat=True),
        'cards': paginated_cards,
        'auth': req.user.is_authenticated})


def login(req):
    return render(req, 'login.html', context={
        'members': Profile.objects.best(),
        'tags': Tag.objects.popular().values_list('name', flat=True)})


def signup(req):
    return render(req, 'signup.html', context={
        'members': Profile.objects.best(),
        'tags': Tag.objects.popular().values_list('name', flat=True)})


def settings(req):
    profile = get_object_or_404(Profile, user_id=req.user.id) if req.user.is_authenticated else None
    return render(req, 'settings.html', context={
        'members': Profile.objects.best(),
        'tags': Tag.objects.popular().values_list('name', flat=True),
        'userpic': profile.avatar.url if profile and profile.avatar else None,
        'username': req.user.username if req.user.is_authenticated else None})


def tag(req, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    questions_with_tag = Question.objects.tag(tag)
    paginated_cards = paginate(questions_with_tag, req, 6)
    profile = get_object_or_404(Profile, user_id=req.user.id) if req.user.is_authenticated else None
    return render(req, 'tag.html', context={
        'members': Profile.objects.best(),
        'tags': Tag.objects.popular().values_list('name', flat=True),
        'userpic': profile.avatar.url if profile and profile.avatar else None,
        'username': req.user.username if req.user.is_authenticated else None,
        'cards': paginated_cards,
        'tag': tag})


def hot(req):
    profile = get_object_or_404(Profile, user_id=req.user.id) if req.user.is_authenticated else None
    paginated_cards = paginate(Question.objects.popular(), req, 4)
    return render(req, 'hot.html', context={
        'members': Profile.objects.best(),
        'tags': Tag.objects.popular().values_list('name', flat=True),
        'userpic': profile.avatar.url if profile and profile.avatar else None,
        'username': req.user.username if req.user.is_authenticated else None,
        'cards': paginated_cards})


def question(req, question_id):
    profile = get_object_or_404(Profile, user_id=req.user.id) if req.user.is_authenticated else None
    question = get_object_or_404(Question.objects.annotate(likes_count=Count('likes')), id=question_id)
    paginated_answers = paginate(Answer.objects.answers(question=question).annotate(likes_count=Count('likes')),
                                 req, 4)
    return render(req, 'question.html', context={
        'members': Profile.objects.best(),
        'tags': Tag.objects.popular().values_list('name', flat=True),
        'userpic': profile.avatar.url if profile and profile.avatar else None,
        'username': req.user.username if req.user.is_authenticated else None,
        'cards': paginated_answers,
        'question': get_object_or_404(Question.objects.annotate(likes_count=Count('likes')), id=question_id),
        'question_id': question_id})


def ask(req):
    profile = get_object_or_404(Profile, user_id=req.user.id) if req.user.is_authenticated else None
    userpic = profile.avatar.url if profile and profile.avatar else None
    return render(req, 'ask.html', context={
        'members': Profile.objects.best(),
        'tags': Tag.objects.popular().values_list('name', flat=True),
        'userpic': userpic,
        'username': req.user.username if req.user.is_authenticated else None})
