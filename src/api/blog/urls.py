from django.urls import path
from src.api.blog.views import *

urlpatterns = [
    path('posts/', PostListAPIView.as_view(), name='posts-list'),
    path('post/<int:id>/', GetPostByIdAPIView.as_view(), name='get_post_by_id'),
    path('categories/', CategoriesWithCountAPIView.as_view(), name='categories-with-posts'),
    path('post/', CreatePostAPIView.as_view(), name='create-post'),
]
