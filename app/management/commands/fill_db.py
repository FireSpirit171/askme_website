import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from faker import Faker
from ...models import User_profile, Tag, Question, Answer, LikeQuestion, LikeAnswer


class Command(BaseCommand):
    help = 'Fills the database with test data based on the given ratio.'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='The fill ratio for test data')

    def handle(self, *args, **kwargs):
        ratio = kwargs['ratio']
        fake = Faker()

        django_users = [User(username=fake.unique.user_name(), email=fake.unique.email(), password=fake.password())
                        for i in range(ratio)]
        User.objects.bulk_create(django_users)

        # Создаем профили пользователей
        user_profiles = [User_profile(user=user, nickname=fake.unique.user_name(), avatar=None)
                         for i, user in enumerate(django_users)]
        User_profile.objects.bulk_create(user_profiles)

        profiles = list(User_profile.objects.all())

        # Создание тэгов
        tags = [Tag(name=f"Tag {i}") for i in range(ratio)]
        Tag.objects.bulk_create(tags)
        tag_list = list(Tag.objects.all())

        # Создание вопросов
        questions = [Question(title=fake.sentence(), text=fake.text(), author=random.choice(profiles)) for _ in
                     range(ratio * 10)]
        Question.objects.bulk_create(questions)
        for question in Question.objects.all():
            question.tag.add(*random.sample(tag_list, min(len(tag_list), random.randint(1, 3))))

        # Создание ответов
        QUESTIONS_CHOICES = list(Question.objects.all())

        answers = []
        for i in range(ratio * 100):
            answers.append(Answer(text=fake.text(), author=random.choice(profiles),
                                  question=random.choice(QUESTIONS_CHOICES)))
        Answer.objects.bulk_create(answers)

        # Создание лайков вопросов
        LIKE_STATUS_CHOICE = ['l', 'd']
        QUESTION_LIKE = []
        used_pairs = set()
        i = 0
        while i != (ratio * 100):
            user = random.choice(profiles)
            question = random.choice(QUESTIONS_CHOICES)
            pair = (user, question)
            if pair not in used_pairs:
                QUESTION_LIKE.append(LikeQuestion(user=user,
                                                  question=question,
                                                  status=random.choice(LIKE_STATUS_CHOICE)))
                used_pairs.add(pair)
                i += 1
        LikeQuestion.objects.bulk_create(QUESTION_LIKE)

        # Создание лайков ответов
        ANSWERS_CHOICES = list(Answer.objects.all())
        ANSWER_LIKE = []
        used_pairs.clear()
        i = 0
        while i != (ratio * 100):
            user = random.choice(profiles)
            answer = random.choice(ANSWERS_CHOICES)
            pair = (user, answer)
            if pair not in used_pairs:
                ANSWER_LIKE.append(LikeAnswer(user=user,
                                              answer=answer,
                                              status=random.choice(LIKE_STATUS_CHOICE)))
                used_pairs.add(pair)
                i += 1
        LikeAnswer.objects.bulk_create(ANSWER_LIKE)

        self.stdout.write(self.style.SUCCESS(f'Successfully added test data with ratio {ratio}.'))
