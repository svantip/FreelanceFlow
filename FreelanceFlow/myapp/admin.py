# Register your models here.
from django.contrib import admin

from .models import *
from .models import Project, Tag, Task

# Register your models here.
admin.site.register(Tag)
admin.site.register(Project)
admin.site.register(Task)
