from django.contrib import admin
from app import models

admin.site.register(models.User_profile)
admin.site.register(models.Tag)
admin.site.register(models.LikeAnswer)
admin.site.register(models.LikeQuestion)
admin.site.register(models.Answer)
admin.site.register(models.Question)
