# create forms to models in board/models.py

from django import forms
from .models import Board, Column, Task


class BoardForm(forms.ModelForm):
    # write code here
    class Meta:
        model = Board
        fields = "__all__"


class ColumnForm(forms.ModelForm):
    # write code here
    class Meta:
        model = Column
        fields = ["title"]


class TaskForm(forms.Form):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "column",
            "priority",
        ]
