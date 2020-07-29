from django.shortcuts import render,redirect,get_object_or_404
from .models import Post,Profile,Comment
from django.contrib.auth.models import User
from django.views.generic import CreateView,UpdateView,DeleteView,ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm,CommentForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse

def home(request):
	context={
		'posts':Post.objects.all()
	}
	return render(request,'blog/home.html',context)

def about(request):
	return render(request,'blog/about.html',{'title':'About'})

def privacy(request):
	return render(request,'blog/privacy.html')

def terms(request):
	return render(request,'blog/terms.html')

def me(request):
	return render(request,'blog/me.html')

def like_post(request, pk):
	post = get_object_or_404(Post, id= request.POST.get('post_id'))
	is_liked = False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		is_liked = False
	else:
		post.likes.add(request.user)
		is_liked = True

	return HttpResponseRedirect(reverse('home'))

def fav_post(request, pk):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	is_favourite = False
	if post.favourites.filter(id=request.user.id).exists():
		post.favourites.remove(request.user)
		is_favourite = False
		return redirect ('home')
	else:
		post.favourites.add(request.user)
		is_favourite = True
	return HttpResponseRedirect(reverse('home'))

def my_like_post(request, pk):
	post = get_object_or_404(Post, id= request.POST.get('post_id'))
	is_liked = False
	if post.likes.filter(id=request.user.id).exists():
		post.likes.remove(request.user)
		is_liked = False
	else:
		post.likes.add(request.user)
		is_liked = True
	return HttpResponseRedirect(post.get_absolute_url())

def my_fav_post(request, pk):
	post = get_object_or_404(Post, id=request.POST.get('post_id'))
	is_favourite = False
	if post.favourites.filter(id=request.user.id).exists():
		post.favourites.remove(request.user)
		is_favourite = False
	else:
		post.favourites.add(request.user)
		is_favourite = True
	return HttpResponseRedirect(post.get_absolute_url())

def myfavpost(request):
	user = request.user
	favourite_posts = user.favourites.all()
	return render(request,'blog/myfavpost.html',{'favourite_posts':favourite_posts})

def register(request):
	if request.method =='POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request,f'{username} Your Account Has Been Created, You Are Now Able To Login !')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request,'blog/register.html',{'form':form})

@login_required
def profile(request):
	if request.method == "POST":
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST,files=request.FILES,instance=request.user.profile)
		if u_form.is_valid() or p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request,f'Your Profile Has Been Updated !!')
			return redirect('profile')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance = request.user.profile)
	return render(request,'blog/profile.html',{'u_form':u_form,'p_form':p_form})

class PostListView(ListView):
	model = Post
	template_name = 'blog/home.html'
	context_object_name = 'posts'
	ordering = ['-date_posted']
	paginate_by = 5

	def get_context_date(self,*args,**kwargs):
		post = get_object_or_404(Post,id=self.kwargs.get('id'))
		total_likes=post.total_likes()
		is_liked = False
		is_favourite = False
		if post.likes.filter(id=self.request.user.id).exists():
			is_liked = True

		if post.favourites.filter(id=self.request.user.id).exists():
			is_favourite = True

		context['total_likes']=total_likes
		context['is_liked']=is_liked
		context['is_favourite']=is_favourite
		return context


	def get_queryset(self):
		result = super(PostListView, self).get_queryset()
		query = self.request.GET.get('search')
		if query:
			postresult = Post.objects.filter(
				Q(title__contains=query) |
				Q(author__username=query) |
				Q(content__contains=query)
				)
			result = postresult
		return result

class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/post_detail.html'


class UserPostListView(ListView):
	model = Post
	template_name = 'blog/user_posts.html'
	context_object_name = 'posts'
	paginate_by = 3

	def get_queryset(self):
		user = get_object_or_404(User,username=self.kwargs.get('username'))
		return Post.objects.filter(author=user).order_by('-date_posted')


class PostCreateView(LoginRequiredMixin,CreateView):
	model = Post
	fields = ['title','content','status']
	success_url = '/'

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

class CommentCreateView(LoginRequiredMixin,CreateView):
	model = Comment
	fields = ['name','body']
	template_name = 'blog/add_comment.html'
	success_url = '/'

	def form_valid(self,form):
		form.instance.post_id = self.kwargs['pk']
		return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,SuccessMessageMixin,UpdateView):
	model = Post
	fields = ['title','content','status']
	success_message = 'Your Post Has Been Updated !!'

	def form_valid(self,form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
	model = Post
	success_url = '/'
	success_message = 'Your Post Has Been Deleted !!'

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.author:
			return True
		return False

	def delete(self,request,*args,**kwargs):
		messages.success(self.request,self.success_message)
		return super(PostDeleteView,self).delete(request,*args,**kwargs)



