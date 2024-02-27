from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from .models import Category, Post, Comment
from .serializers import CategorySerializer, PostSerializer, CommentSerializer
from .forms import CommentForm


# Template Views
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'blog/category_list.html', {'categories': categories})


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'blog/category_detail.html', {'category': category})


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Filter and serialize only approved comments
    approved_comments = post.comments.filter(approved=True)
    serializer = PostSerializer(post)
    return render(request, 'blog/post_detail.html', {'post': post, 'approved_comments': approved_comments})


def comment_view(request, post_id):
    if request.method == "POST":
        # Retrieve data from the form
        author = request.POST.get("author", "")
        comment_text = request.POST.get("comment", "")

        # Perform any necessary validation here

        # Create a new Comment instance and save it to the database
        comment = Comment(
            author=author, body=comment_text, post=Post.objects.get(id=post_id)
        )
        comment.save()

        # Redirect to a success page or the same page with a success message
        return redirect(reverse("post_detail", args=[post_id]))
    else:
        return redirect(reverse("post_detail", args=[post_id]))
    

# API Views
@api_view(['GET'])
def api_category_list(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    serializer = CategorySerializer(category)
    return Response(serializer.data)


@api_view(['GET'])
def api_post_list(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    serializer = PostSerializer(post)
    return Response(serializer.data)

    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_comment_list(request, post_id):
    if request.method == 'GET':
        comments = Comment.objects.filter(post_id=post_id, approved=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = {'author': request.user.id, 'post': post_id, 'text': request.data.get('text'), 'approved': False}
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return redirect('blog:post_detail', post_id=post_id)  # Redirect to the post_detail page
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def api_comment_detail(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    elif request.method == 'PUT':
        comment.approved = True
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
