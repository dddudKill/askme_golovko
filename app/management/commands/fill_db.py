from django.core.management.base import BaseCommand
from faker import Faker
from app.models import Question, Tag, Answer, Profile, User

faker = Faker()


def get_ratios(ratio):
    ratios = {
        'USERS': ratio,
        'QUESTIONS': ratio * 10,
        'ANSWERS': ratio * 100,
        'TAGS': ratio,
        'LIKES': ratio * 200,
    }
    return ratios


RATIO_DEFAULT = 10000

RATIOS_DEFAULT = get_ratios(RATIO_DEFAULT)

BATCH_SIZE = 2000


class Command(BaseCommand):
    help = 'Fill the database'

    def fill_users(self, ratio):
        if User.objects.count() >= 2*RATIOS_DEFAULT['USERS']:
            return

        users_temp = []

        for i in range(1, ratio):
            user_data = {"username": faker.unique.user_name(), "mail": faker.email()}
            users_temp.append(
                User(
                    is_superuser=False,
                    username=user_data['username'],
                    email=user_data['mail'],
                    password='password'
                )
            )
            if i % BATCH_SIZE == 0:
                User.objects.bulk_create(users_temp, BATCH_SIZE)
                users_temp = []
        User.objects.bulk_create(users_temp)

    def fill_profiles(self):
        if Profile.objects.count() >= 2*RATIOS_DEFAULT['USERS']:
            return

        users_data = User.objects.all()
        profiles_temp = []

        for i in range(1, len(users_data)):
            avatar_path = f'profile_pics/avatar{faker.random_int(1, 3)}.jpg'
            try:
                users_data[i].profile.DoesNotExist()
                continue
            except:
                profiles_temp.append(
                    Profile(
                        user=users_data[i],
                        nickname=users_data[i].username,
                        avatar=avatar_path
                    )
                )
                if i % BATCH_SIZE == 0:
                    Profile.objects.bulk_create(profiles_temp, BATCH_SIZE)
                    profiles_temp = []
        Profile.objects.bulk_create(profiles_temp)

    def fill_tags(self, ratio):
        if Tag.objects.count() >= 2*RATIOS_DEFAULT['TAGS']:
            return
        tags_temp = []

        for i in range(1, ratio):
            tag_data = {
                "name": faker.unique.user_name()[:6],
                "rating": faker.random_int(0, 60)
            }
            tags_temp.append(
                Tag(
                    name=tag_data['name'],
                    rating=tag_data['rating']
                )
            )
            if i % BATCH_SIZE == 0:
                Tag.objects.bulk_create(tags_temp, BATCH_SIZE)
                tags_temp = []
        Tag.objects.bulk_create(tags_temp)

    def fill_questions(self, ratio):
        if Question.objects.count() >= 2*RATIOS_DEFAULT['QUESTIONS']:
            return

        questions_temp = []
        profiles_data = Profile.objects.all()
        tags_data = Tag.objects.all()

        for i in range(1, ratio):

            question_data = {
                "title": faker.unique.sentence(6),
                "text": faker.unique.paragraph(6),
                "author": profiles_data[faker.random_int(0, len(profiles_data) - 1)],
                "rating": faker.random_int(-20, 20)
            }
            questions_temp.append(
                Question(
                    title=question_data['title'],
                    text=question_data['text'],
                    author=question_data['author'],
                    rating=question_data['rating']
                )
            )
            if i % BATCH_SIZE == 0:
                Question.objects.bulk_create(questions_temp, BATCH_SIZE)
                questions_temp = []
        Question.objects.bulk_create(questions_temp)

        for question in Question.objects.all().filter(tags__exact=None):
            tags_spec = []
            for j in range(faker.random_int(1, Question.tags.field.max_length)):
                tags_spec.append(tags_data[faker.random_int(0, len(tags_data) - 1)])
            question.tags.set(tags_spec)

    def fill_answers(self, ratio):
        if Answer.objects.count() >= 2*RATIOS_DEFAULT['ANSWERS']:
            return

        answers_temp = []
        questions_data = Question.objects.all()
        profiles_data = Profile.objects.all()

        for i in range(1, ratio):

            answer_data = {
                "question": questions_data[faker.random_int(0, len(questions_data) - 1)],
                "text": faker.unique.paragraph(6),
                "author": profiles_data[faker.random_int(0, len(profiles_data) - 1)],
                "rating": faker.random_int(-20, 20)
            }

            answers_temp.append(
                Answer(
                    author=answer_data['author'],
                    text=answer_data['text'],
                    rating=answer_data['rating'],
                    question=answer_data['question']
                )
            )
            if i % BATCH_SIZE == 0:
                Answer.objects.bulk_create(answers_temp, BATCH_SIZE)
                answers_temp = []
        Answer.objects.bulk_create(answers_temp)

    def fill_likes(self, ratio):
        questions_data = Question.objects.all()
        answers_data = Answer.objects.all()
        questions_to_update = []
        answers_to_update = []

        for i in range(1, ratio):
            value = -1 if faker.random_int(0, 1) == 0 else 1
            if faker.random_int(0, 1) == 0:
                question = questions_data[faker.random_int(0, len(questions_data) - 1)]
                question.rating += value
                questions_to_update.append(question)
            else:
                answer = answers_data[faker.random_int(0, len(answers_data) - 1)]
                answer.rating += value
                answers_to_update.append(answer)
            if i % (BATCH_SIZE * 2) == 0:
                Question.objects.bulk_update(questions_to_update, ['rating'], BATCH_SIZE)
                questions_to_update = []
                Answer.objects.bulk_update(answers_to_update, ['rating'], BATCH_SIZE)
                answers_to_update = []

        Question.objects.bulk_update(questions_to_update, ['rating'])
        Answer.objects.bulk_update(answers_to_update, ['rating'])

    def update_profiles_ratings(self):
        profiles_data = Profile.objects.all()

        i = 0
        for profile in profiles_data:
            i += 1
            profile.update_rating()

    def update_tags_ratings(self):
        tags_data = Tag.objects.all()

        i = 0
        for tag in tags_data:
            i += 1
            tag.update_rating()

    def handle(self, *args, **options):
        ratios = get_ratios(ratio=options['ratio'])
        print(ratios)
        self.fill_users(ratios['USERS'])
        self.fill_profiles()
        self.fill_tags(ratios['TAGS'])
        self.fill_questions(ratios['QUESTIONS'])
        self.fill_answers(ratios['ANSWERS'])
        self.fill_likes(ratios['LIKES'])
        self.update_profiles_ratings()
        self.update_tags_ratings()

    def add_arguments(self, parser):
        parser.add_argument(
            'ratio',
            nargs='?',
            type=int,
            action='store',
            default=100
        )
