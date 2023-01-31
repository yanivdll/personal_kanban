from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Board(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Boards"
        ordering = ["id"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("board:board", args=[str(self.pk)])


class Column(models.Model):
    title = models.CharField(max_length=255)
    board = models.ForeignKey("Board", related_name="columns", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Task(models.Model):
    class Priority(models.TextChoices):
        HIGH = "H", "High"
        MEDIUM = "M", "Medium"
        LOW = "L", "Low"

    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(
        max_length=1,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )
    board = models.ForeignKey("Board", related_name="tasks", on_delete=models.CASCADE)
    column = models.ForeignKey("Column", related_name="tasks", on_delete=models.CASCADE)
    task_order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    def __str__(self):
        return f"{self.id} - {self.title}"

    class Meta:
        ordering = ["task_order"]
        verbose_name_plural = "Tasks"
