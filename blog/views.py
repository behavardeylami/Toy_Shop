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

# def comment_list(request, post_id):
#     comments = Comment.objects.filter(post_id=post_id, approved=True)
#     return render(request, 'comments_list.html', {'comments': comments})

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

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def api_comment_list(request, post_id):
#     if request.method == 'GET':
#         comments = Comment.objects.filter(post_id=post_id, approved=True)
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         data = {'author': request.user.id, 'post': post_id, 'text': request.data.get('text'), 'approved': False}
#         serializer = CommentSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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

# from django.shortcuts import get_object_or_404
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated
# from django.urls import reverse
# from .models import Category, Post, Comment
# from .serializers import CategorySerializer, PostSerializer, CommentSerializer
# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Category, Post, Comment
# from .forms import CommentForm


# def category_list(request):
#     categories = Category.objects.all()
#     return render(request, 'categories_list.html', {'categories': categories})


# def category_detail(request, category_id):
#     category = get_object_or_404(Category, id=category_id)
#     return render(request, 'category_detail.html', {'category': category})


# def post_list(request):
#     posts = Post.objects.all()
#     return render(request, 'posts_list.html', {'posts': posts})


# def comment_view(request, post_id):
#     if request.method == "POST":
#         # Retrieve data from the form
#         author = request.POST.get("author", "")
#         comment_text = request.POST.get("comment", "")

#         # Perform any necessary validation here

#         # Create a new Comment instance and save it to the database
#         comment = Comment(
#             author=author, body=comment_text, post=Post.objects.get(id=post_id)
#         )
#         comment.save()

#         # Redirect to a success page or the same page with a success message
#         return redirect(reverse("post_detail", args=[post_id]))
#     else:
#         return redirect(reverse("post_detail", args=[post_id]))


# def comment_list(request, post_id):
#     comments = Comment.objects.filter(post_id=post_id, approved=True)
#     return render(request, 'comments_list.html', {'comments': comments})


# # Views for Categories
# @api_view(['GET'])
# def category_list(request):
#     categories = Category.objects.all()
#     serializer = CategorySerializer(categories, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def category_detail(request, category_id):
#     category = get_object_or_404(Category, id=category_id)
#     serializer = CategorySerializer(category)
#     return Response(serializer.data)


# # Views for Posts
# @api_view(['GET'])
# def post_list(request):
#     posts = Post.objects.all()
#     serializer = PostSerializer(posts, many=True)
#     return Response(serializer.data)


# @api_view(['GET'])
# def post_detail(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     # Filter and serialize only approved comments
#     approved_comments = post.comments.filter(approved=True)
#     post.comments = approved_comments
#     serializer = PostSerializer(post)
#     return Response(serializer.data)


# # Views for Comments
# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def comment_list(request, post_id):
#     if request.method == 'GET':
#         comments = Comment.objects.filter(post_id=post_id, approved=True)
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         data = {'author': request.user.id, 'post': post_id, 'text': request.data.get('text'), 'approved': False}
#         serializer = CommentSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# # View for Comment Detail and Approval
# @api_view(['GET', 'PUT'])
# @permission_classes([IsAuthenticated])
# def comment_detail(request, comment_id):
#     comment = get_object_or_404(Comment, id=comment_id)

#     if request.method == 'GET':
#         serializer = CommentSerializer(comment)
#         return Response(serializer.data)

#     elif request.method == 'PUT':
#         comment.approved = True
#         comment.save()
#         serializer = CommentSerializer(comment)
#         return Response(serializer.data)



# from django.shortcuts import render, get_object_or_404, redirect
# from rest_framework import generics
# from .serializers import CategorySerializer, PostSerializer, CommentSerializer
# from django.contrib import messages
# from django.views import View
# from .models import Category, Post, Comment
# from .forms import CommentForm


# class CategoryListAPIView(generics.ListAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


# class CategoryDetailAPIView(generics.RetrieveAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer


# class PostListAPIView(generics.ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# class PostDetailAPIView(generics.RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer


# class CommentCreateAPIView(generics.CreateAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer


# class CategoryListView(View):
#     def get(self, request):
#         categories = Category.objects.all()
#         return render(request, 'blog/category_list.html', {'categories': categories})


# class CategoryDetailView(View):
#     def get(self, request, category_id):
#         category = get_object_or_404(Category, pk=category_id)
#         posts = category.posts.all()
#         return render(request, 'blog/category_detail.html', {'category': category, 'posts': posts})


# class PostListView(View):
#     def get(self, request):
#         posts = Post.objects.all()
#         return render(request, 'blog/post_list.html', {'posts': posts})


# class PostDetailView(View):
#     def get(self, request, post_id):
#         post = get_object_or_404(Post, pk=post_id)
#         comments = Comment.objects.filter(post=post, is_active=True)
#         comment_form = CommentForm()  # Assuming you have a CommentForm defined in forms.py
#         return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})


# class CommentListView(View):
#     template_name = 'comment_list.html'  # نام قالب HTML برای نمایش لیست نظرات

#     def get(self, request, post_id):
#         post = get_object_or_404(Post, id=post_id)
#         comments = Comment.objects.filter(post=post, is_approved=True)
#         return render(request, self.template_name, {'post': post, 'comments': comments})
# # class CommentCreateView(request, post_id):
# #     if request.method == "POST":
# #         # Retrieve data from the form
# #         author = request.POST.get("author", "")
# #         comment_text = request.POST.get("comment", "")

# #         # Perform any necessary validation here

# #         # Create a new Comment instance and save it to the database
# #         comment = Comment(
# #             author=author, body=comment_text, post=Post.objects.get(id=post_id)
# #         )
# #         comment.save()

# #         # Redirect to a success page or the same page with a success message
# #         return redirect(reverse("post_detail", args=[post_id]))
# #     else:
# #         return redirect(reverse("post_detail", args=[post_id]))
    

#     # def post(self, request, post_id):
#     #     post = get_object_or_404(Post, pk=post_id)
#     #     form = CommentForm(request.POST)

#     #     if form.is_valid():
#     #         comment = form.save(commit=False)
#     #         comment.author = request.user
#     #         comment.save()
#     #         return redirect('post_detail', post_id=post_id)

#     #     else:
#     #         return redirect('some_other_view')
        
#         #     comment.post.add(post)

#         #     messages.success(request, 'Your comment has been successfully submitted')

#         #     return redirect('post_detail', post_id=post_id)

#         # return render(request, 'blog/comment_form.html', {'comment_form': comment_form})
