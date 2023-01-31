from django.contrib import admin
from .models import Board, Column, Task, User

# Register your models here.
# admin.site.register(User)
admin.site.register(Board)
admin.site.register(Column)
admin.site.register(Task)
