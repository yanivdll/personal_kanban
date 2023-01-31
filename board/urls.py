from django.urls import path
from . import views

app_name = "board"
urlpatterns = [
    path("", views.index, name="index"),
    path("boards/", views.BoardListView.as_view(), name="boards"),
    path("board/<int:pk>/", views.BoardDetailView.as_view(), name="board"),
    path("board/create/", views.BoardCreateView.as_view(), name="create_board"),
    path(
        "board/<int:pk>/update/", views.BoardUpdateView.as_view(), name="update_board"
    ),
    # path("board/<int:pk>/delete/", views.BoardDeleteView.as_view(), name="delete_board"),
    path(
        "board/<int:board_id>/column/create/",
        views.ColumnCreateView.as_view(),
        name="create_column",
    ),
    # path(
    #     "board/<int:board_id>/column/<int:pk>/update/",
    #     views.ColumnUpdate.as_view(),
    #     name="update_column",
    # ),
    # path(
    #     "board/<int:board_id>/column/<int:pk>/delete/",
    #     views.ColumnDelete.as_view(),
    #     name="delete_column",
    # ),
    path(
        "board/<int:board_id>/task/<int:pk>/",
        views.TaskDetailView.as_view(),
        name="task",
    ),
    path(
        "board/<int:board_id>/column/<int:column_id>/task/create/",
        views.TaskCreateView.as_view(),
        name="create_task",
    ),
    path(
        "board/<int:board_id>/task/<int:task_id>/update/",
        views.TaskUpdateView.as_view(),
        name="update_task",
    ),
    path(
        "board/<int:board_id>/task/<int:task_id>/delete/",
        views.TaskDeleteView.as_view(),
        name="delete_task",
    ),
]
