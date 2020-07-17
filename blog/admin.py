from django.contrib import admin
from .models import Post, Profile, Comment

class PostAdmin(admin.ModelAdmin):
	list_display = ('title','author','status')
	list_filter = ('status','author','date_posted')
	search_fields = ('author__username','title')
	list_editable = ('status',)
	date_hierarchy = ('date_posted')

class ProfileAdmin(admin.ModelAdmin):
	list_display=('user','image')

admin.site.register(Post,PostAdmin)
admin.site.register(Comment)
admin.site.register(Profile,ProfileAdmin)
