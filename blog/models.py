from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

STATUS = ((0,"Draft"),(1,"Publish"))

class Post(models.Model):
	title = models.CharField(max_length = 100)
	content = models.TextField(blank=True, null=True)
	date_posted = models.DateTimeField(auto_now_add = True)
	author = models.ForeignKey(User,on_delete = models.CASCADE)
	status = models.IntegerField(choices = STATUS, default = 0)
	likes = models.ManyToManyField(User, related_name ='likes', blank=True)
	favourites = models.ManyToManyField(User, related_name='favourites',blank = True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail',kwargs={'pk':self.pk})

	def total_likes(self):
		return self.likes.count()

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	image = models.ImageField(default = 'default.jpg',null = True, blank = True)

	def __str__(self):
		return f'{self.user.username} Profile'

class Comment(models.Model):
	post = models.ForeignKey(Post,on_delete = models.CASCADE,related_name='comments')
	name = models.CharField(max_length = 255, null = True)
	body = models.TextField(blank=True,null=True)
	timestamp = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return '{}-{}'.format(self.post.title, self.name)
