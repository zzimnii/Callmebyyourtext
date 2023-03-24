from django.contrib import admin
from .models import Question, Comment, BeQuestion, RecQuestion, BeComment


admin.site.register(Question)
admin.site.register(RecQuestion)
admin.site.register(BeQuestion)
admin.site.register(Comment)
admin.site.register(BeComment)