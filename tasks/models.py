from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Task(models.Model):
    class Status(models.TextChoices):
        CREATED = 'created', 'Created'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'

    PRIORITY_CHOICES = [(i, str(i)) for i in range(1, 6)]

    title = models.CharField(max_length=200)
    description = models.TextField()
    deadline = models.DateTimeField()
    priority = models.IntegerField(choices=PRIORITY_CHOICES, default=3)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    categories = models.ManyToManyField(Category, related_name="tasks")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task-detail', kwargs={'pk': self.pk})

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return f"Comment by {self.user.username} on {self.task.title}"