from django.contrib import admin
from gallery.models import Post

# Register your models here.


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'slug', 'text', 'author', 'created_date']
    ordering = ['-created_date']


admin.site.register(Post, PhotoAdmin)
