from django.contrib import admin
from .models import Project, Team, Task, Feedback

admin.site.register(Project)
admin.site.register(Team)
admin.site.register(Task)
admin.site.register(Feedback)

