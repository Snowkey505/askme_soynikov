from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Profile, Question, Answer, Tag, QuestionLike, AnswerLike
from faker import Faker
import random
from django.db import transaction

fake = Faker()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Коэффициент заполнения данных')

    @transaction.atomic
    def handle(self, *args, **options):
        ratio = options['ratio']
        profiles = self.create_users(ratio)
        tags = self.create_tags(ratio)
        questions = self.create_questions(ratio, tags, profiles)
        self.create_answers(ratio, questions, profiles)
        self.create_likes(ratio, questions, profiles)
        self.stdout.write(self.style.SUCCESS('База данных успешно заполнена!'))

    def create_users(self, ratio):
        users = [User(username=fake.unique.user_name(), email=fake.unique.email()) for _ in range(ratio)]
        User.objects.bulk_create(users)
        profiles = [Profile(user=user, avatar=None) for user in User.objects.order_by('-id')[:ratio]]
        Profile.objects.bulk_create(profiles)
        return Profile.objects.order_by('-id')[:ratio]

    def create_tags(self, ratio):
        tags = set()
        while len(tags) < ratio + 1:
            tags.add(f"{fake.word()}_{random.randint(0, 100)}")
        Tag.objects.bulk_create([Tag(name=name) for name in tags])
        return Tag.objects.all()

    def create_questions(self, ratio, tags, profiles):
        title_pool = [fake.sentence() for _ in range(1000)]
        text_pool = [fake.text() for _ in range(1000)]
        questions = [Question(user=profile, title=random.choice(title_pool), text=random.choice(text_pool))
                     for profile in profiles for _ in range(10)]
        Question.objects.bulk_create(questions)
        questions = Question.objects.all()
        for question in questions:
            question.tags.add(*random.sample(tags, random.randint(5, 10)))
        return questions

    def create_answers(self, ratio, questions, profiles):
        text_pool = [fake.text() for _ in range(1000)]
        answers = []
        for question in questions:
            has_correct_answer = False
            for _ in range(10):
                profile = random.choice(profiles)
                correct = random.random() < 0.1 and not has_correct_answer
                has_correct_answer = has_correct_answer or correct
                answers.append(Answer(question=question, user=profile, text=random.choice(text_pool), correct=correct))
            question.answers_count = 10
        Question.objects.bulk_update(questions, ['answers_count'])
        for i in range(0, len(answers), 10000):
            Answer.objects.bulk_create(answers[i:i + 10000])

    def create_likes(self, ratio, questions, profiles):
        question_likes = [QuestionLike(user=random.choice(profiles), question=random.choice(questions))
                          for _ in range(ratio * 200)]
        QuestionLike.objects.bulk_create(question_likes, ignore_conflicts=True)
        answers = Answer.objects.all()
        answer_likes = [AnswerLike(user=random.choice(profiles), answer=random.choice(answers))
                        for _ in range(ratio * 200)]
        AnswerLike.objects.bulk_create(answer_likes, ignore_conflicts=True)
