from django.urls import path,include
from . import views
from . import views as user_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from .views import PostDetailView,PostCreateView,PostUpdateView,PostDeleteView,PostListView,UserPostListView

urlpatterns = [
    path('',PostListView.as_view(),name='home'),
    path('about/',views.about, name = 'about'),
    path('user/<str:username>',UserPostListView.as_view(),name ='user-posts'),
    path('register/',user_views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name='blog/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='blog/logout.html'),name='logout'),
    path('profile/',user_views.profile,name='profile'),
    path('post/<int:pk>/',PostDetailView.as_view(),name='post-detail'),
    path('post/new/',PostCreateView.as_view(),name='post-create'),
    path('post/<int:pk>/update/',PostUpdateView.as_view(),name='post-update'),
    path('post/<int:pk>/delete/',PostDeleteView.as_view(),name='post-delete'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='blog/password_reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='blog/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='blog/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='blog/password_reset_complete.html'),name='password_reset_complete'),
    path('oauth/',include('social_django.urls',namespace='social')),
    path('like/<int:pk>',views.like_post, name='like_post'),
    path('fav/<int:pk>',views.fav_post,name='fav_post'),
    path('mylike/<int:pk>',views.my_like_post,name='my_like_post'),
    path('myfav/<int:pk>',views.my_fav_post,name='my_fav_post'),
    path('myfavpost/',views.myfavpost,name='myfavpost'),
    path('privacy/',views.privacy,name='privacy'),
    path('terms/',views.terms,name='terms'),
    path('me/',views.me,name='me'),
]


if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
