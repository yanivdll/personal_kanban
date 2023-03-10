import json
import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.urls import reverse
from django.views import View, generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import BoardForm, ColumnForm, TaskForm
from .models import Board, Column, Task


def index(request):
    boards = Board.objects.all()
    template = loader.get_template(template_name="board/index.html")

    number_of_visits = request.session.get("number_of_visits", 0)
    request.session["number_of_visits"] = number_of_visits + 1
    print(f"Number of visits: {number_of_visits}")
    context = {"boards": boards, "number_of_visits": number_of_visits}
    return render(request, "board/index.html", context)


# BOARD views
class BoardListView(LoginRequiredMixin, generic.ListView):
    model = Board
    template_name = "board/boards.html"
    context_object_name = "boards"

    def get_queryset(self):
        return Board.objects.filter(owner=self.request.user)


class BoardDetailView(LoginRequiredMixin, generic.DetailView):
    model = Board
    template_name = "board/board.html"
    context_object_name = "board"

    # Overriding the get_queryset method to filter the boards by the owner and restrict access to the boards for users who are not the owner.
    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)


class BoardCreateView(LoginRequiredMixin, CreateView):
    model = Board
    template_name = "board/board_create.html"
    fields = ["name", "description"]

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("board:board", args=[self.object.id])


class BoardUpdateView(LoginRequiredMixin, UpdateView):
    model = Board
    template_name = "board/board_update.html"
    fields = ["name", "description"]

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    def get_success_url(self):
        return reverse("board:board", args=[self.object.id])


# COLUMN views


class ColumnCreateView(LoginRequiredMixin, CreateView):
    model = Column
    template_name = "board/column_create.html"
    fields = ["title"]

    def get_success_url(self):
        return reverse("board:board", args=[self.kwargs.get("board_id")])

    def form_valid(self, form):
        form.instance.board = Board.objects.get(id=self.kwargs["board_id"])
        return super().form_valid(form)


# TASK views


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task
    template_name = "board/task.html"
    context_object_name = "task"

    def get_queryset(self):
        return self.model.objects.filter(board__owner=self.request.user)


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "board/task_create.html"
    fields = ["title", "description", "priority"]

    def get_success_url(self):
        return reverse("board:board", args=[self.kwargs.get("board_id")])

    def form_valid(self, form):
        form.instance.column = Column.objects.get(id=self.kwargs["column_id"])
        form.instance.board = self.get_board()
        return super().form_valid(form)

    def get_board(self):
        board_id = self.kwargs.get("board_id")
        return Board.objects.get(id=board_id)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "board/task_update.html"
    fields = ["title", "description", "priority"]
    pk_url_kwarg = "task_id"

    def get_success_url(self):
        return reverse("board:board", args=[self.kwargs.get("board_id")])

    def get_queryset(self):
        return self.model.objects.filter(board=self.get_board())

    def get_board(self):
        board_id = self.kwargs.get("board_id")
        return Board.objects.get(id=board_id)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "board/task_delete.html"
    pk_url_kwarg = "task_id"

    def get_success_url(self):
        return reverse("board:board", args=[self.kwargs.get("board_id")])

    def get_queryset(self):
        return self.model.objects.filter(board=self.get_board())

    def get_board(self):
        board_id = self.kwargs.get("board_id")
        return Board.objects.get(id=board_id)


def update_task_ajax(request):
    if request.method == "POST":
        body = json.loads(request.body)
        task_id = body.get("task_id")
        column_id = body.get("column_id")
        try:
            task = Task.objects.get(pk=task_id)
            column = Column.objects.get(pk=column_id)
        except Task.DoesNotExist:
            return JsonResponse({"status": "error"})
        task.column = column
        task.save()
        return JsonResponse({"status": "success"})
