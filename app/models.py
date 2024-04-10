from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Sum, Case, When, IntegerField, Count
from django.shortcuts import get_object_or_404

class QuestionManager(models.Manager):
    def get_hot(self):
        #questions = annotate_likes_question(Question.objects.all())
        #return questions.order_by('-num_likes')
        return self.order_by('-num_likes')

    def get_new(self):
        #questions = annotate_likes_question(Question.objects.all())
        #return questions.order_by('-created_at')
        return self.order_by('-created_at')

    
    def by_tag(self, tag_name):
        #questions = annotate_likes_question(Question.objects.filter(tag__name=tag_name))
        questions = Question.objects.filter(tag__name=tag_name)
        return questions

    def get_one_question(self, question_id):
        #questions = annotate_likes_question(Question.objects.filter(id=question_id))
        questions = Question.objects.filter(id=question_id)
        return questions.get(id=question_id)
    
class AnswerManager(models.Manager):
    def by_question(self, question_id):
        #answers = annotate_likes_answer(Answer.objects.filter(question__id=question_id))
        answers = Answer.objects.filter(question__id=question_id)
        return answers.order_by('-num_likes')

'''    
class TagManager(models.Manager):
    def popular_tags(self):
        return self.order_by('created_at')
'''

class MemberManager(models.Manager):
    def get_member(self, member_name):
        try:
            user_profile = self.annotate(num_likes=Count('likequestion', distinct=True) + Count('likeanswer', distinct=True)).get(nickname=member_name)
        except User_profile.DoesNotExist:
            return get_object_or_404(User_profile, nickname=member_name)
        return user_profile

class User_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    avatar = models.ImageField(null=True, blank=True, upload_to='uploads/')
    nickname = models.CharField(max_length=255)
    activity = models.IntegerField(default=0)

    objects = MemberManager()

    def __str__(self):
        return self.nickname

class Tag(models.Model):
    name = models.CharField(max_length=100)
    num_questions = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #objects = TagManager()

    def __str__(self):
        return self.name

class Question(models.Model):
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey(User_profile, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, blank=True)
    num_likes = models.IntegerField(default=0)
    num_answers = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = QuestionManager()

    def __str__(self):
        return self.title

class Answer(models.Model):
    STATUS_CHOICES = [("m", "Marked as right"), ("nm", "Not marked")]
    text = models.TextField()
    author = models.ForeignKey(User_profile, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10,default='nm')
    num_likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = AnswerManager()

    def __str__(self):
        return self.text
 
class LikeAnswer(models.Model):
    STATUS_CHOICES = [("l", "Like"), ("d", "Dislike")]
    user = models.ForeignKey(User_profile, on_delete=models.CASCADE,default='')
    status = models.CharField(choices=STATUS_CHOICES, max_length=10,default='d')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.nickname
    
    class Meta:
        unique_together = ('user', 'answer')

class LikeQuestion(models.Model):
    STATUS_CHOICES = [("l", "Like"), ("d", "Dislike")]
    user = models.ForeignKey(User_profile, on_delete=models.CASCADE,default='')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10,default='d')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.nickname
    
    class Meta:
        unique_together = ('user', 'question')


