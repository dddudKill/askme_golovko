from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
from django.http import Http404


class TagManager(models.Manager):
    def get_top_tags(self):
        return self.all().order_by('-rating')[:6]

    def get_tag(self, tag_id):
        try:
            return self.get(id=tag_id)
        except Tag.DoesNotExist:
            raise Http404


class Tag(models.Model):
    name = models.CharField(max_length=30)
    rating = models.IntegerField(default=0)

    objects = TagManager()

    def __str__(self):
        return self.name

    def update_rating(self):
        rating_from_questions = self.questions.count()
        self.rating = rating_from_questions
        self.save(update_fields=['rating'])
        return self.rating


class ProfileManager(models.Manager):
    def get_top_profiles(self):
        return self.all().order_by('-rating')[:10]

    def get_profile(self, profile_nickname):
        try:
            return self.get(nickname=profile_nickname)
        except Profile.DoesNotExist:
            raise Http404


class Profile(models.Model):
    nickname = models.CharField(max_length=30)
    avatar = models.ImageField(upload_to='profile_pics', default='profile_pics/avatar_default.jpg', blank=True)
    rating = models.IntegerField(default=0, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', primary_key=True)

    objects = ProfileManager()

    def __str__(self):
        return self.nickname

    def update_rating(self):
        rating_from_questions = self.questions.aggregate(Sum('rating', default=0))['rating__sum']
        rating_from_answers = self.answers.aggregate(Sum('rating', default=0))['rating__sum']
        if type(rating_from_answers) is None:
            print("a is none")
            rating_from_answers = int(0)
        if type(rating_from_questions) is None:
            print("q is none")
            rating_from_questions = int(0)
        self.rating = rating_from_questions + rating_from_answers
        self.save(update_fields=['rating'])
        return self.rating


class QuestionManager(models.Manager):
    def get_new_questions(self):
        return self.all().order_by('-created_date')

    def get_hot_questions(self):
        return self.all().order_by('-rating')

    def get_question(self, question_id):
        try:
            return self.get(id=question_id)
        except Question.DoesNotExist:
            raise Http404

    def get_questions_by_tag(self, tag):
        questions = self.filter(tags__tag__iexact=tag)
        if not questions:
            raise Http404
        return questions


class AnswerManager(models.Manager):
    def get_most_popular(self, question):
        return self.filter(question=question).order_by('-is_correct', '-score')


class Question(models.Model):
    title = models.CharField(max_length=1000)
    text = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='questions', blank=True, max_length=6)
    author = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name='questions')
    rating = models.IntegerField(default=0)
    created_date = models.DateField(auto_now_add=True)

    objects = QuestionManager()

    def __str__(self):
        return f'Title: {self.title}'


class Answer(models.Model):
    author = models.ForeignKey(Profile, null=True, on_delete=models.SET_NULL, related_name='answers')
    text = models.TextField()
    rating = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    is_correct = models.BooleanField(default=False)

    objects = AnswerManager()

    def __str__(self):
        return f'Author: {self.author}, question: {self.question}'
