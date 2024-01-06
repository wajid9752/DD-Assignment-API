from django.db import models
from account.models import BaseClass


class Project(BaseClass):
    name        = models.CharField(max_length=255)
    description = models.TextField()
    start_date  = models.DateField()
    end_date    = models.DateField()
    manager     = models.ForeignKey("account.User", on_delete=models.CASCADE, limit_choices_to={'role': 'manager'},related_name="manager_project")
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Team(BaseClass):
    project = models.ForeignKey("manager.Project", on_delete=models.CASCADE , related_name="teamProjects")
    name = models.CharField(max_length=255)
    members = models.ManyToManyField("account.User", limit_choices_to={'role': 'employee'} , related_name="team_members")
    manager = models.ForeignKey("account.User", on_delete=models.CASCADE, limit_choices_to={'role': 'manager'},related_name="team_manager")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
    
class Task(BaseClass):
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    priority = models.CharField(max_length=20, choices=[('High', 'High'), ('Medium', 'Medium'), ('Low', 'Low')])
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Completed', 'Completed')])
    assigned_to = models.ForeignKey("account.User", on_delete=models.CASCADE, limit_choices_to={'role': 'employee'} , related_name="my_task")
    project = models.ForeignKey("manager.Project", on_delete=models.CASCADE , related_name="emp_task")

    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return self.title
    
    
class Feedback(BaseClass):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    feedback_text = models.TextField()
    created_by = models.ForeignKey("account.User", on_delete=models.CASCADE, limit_choices_to={'role': 'manager'})
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.feedback_text