from django.contrib import admin
from .models import Post, Category, Comments, Contact, Tag


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image', 'is_published', 'views', 'created_at')
    list_display_links = ('id', 'title')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'is_published', 'created_at')
    list_display_links = ('id', 'name')

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'is_solved', 'created_at')
    list_display_links = ('id', 'name')


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag )
admin.site.register(Comments, CommentAdmin)
admin.site.register(Contact, ContactAdmin)