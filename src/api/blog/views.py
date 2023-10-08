from django.db.models import OuterRef, Count, Subquery, IntegerField
from django.db.models.functions import Coalesce
from drf_yasg.openapi import IN_QUERY, TYPE_STRING, Parameter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import PostSerializer, CategoryWithCountSerializer, CreatePostSerializer
from ...blog.models import Post, Category


class PostListAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializer
    search_fields = ['category__slug']
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        queryset = super().get_queryset().filter(is_published=True)
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset

    @swagger_auto_schema(
        manual_parameters=[
            Parameter('category', IN_QUERY, description="category", type=TYPE_STRING)
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class GetPostByIdAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'


class CategoriesWithCountAPIView(generics.ListAPIView):
    serializer_class = CategoryWithCountSerializer
    pagination_class = None  # Disable pagination

    def get_queryset(self):
        # Subquery to count published posts for each category
        subquery = Post.objects.filter(
            category=OuterRef('pk'),
            is_published=True
        ).values('category').annotate(published_post_count=Count('pk')).values('published_post_count')

        # Get all categories and annotate with the count
        queryset = Category.objects.annotate(
            published_post_count=Coalesce(Subquery(subquery, output_field=IntegerField()), 0)
        )
        return queryset


class CreatePostAPIView(APIView):
    @swagger_auto_schema(
        request_body=CreatePostSerializer(),
        responses={
            status.HTTP_201_CREATED: CreatePostSerializer(),
        }
    )
    def post(self, request, format=None):
        serializer = CreatePostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
