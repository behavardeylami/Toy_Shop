from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.urls import reverse
from .models import Category, Product, Comment
from .serializers import CategorySerializer, ProductSerializer, CommentSerializer
from .forms import CommentForm

# Template Views
def category_list(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = category.products.all()
    return render(request, 'store/category_detail.html', {'category': category, 'products': products})


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'store/category_detail.html', {'category': category})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    # Filter and serialize only approved comments
    approved_comments = product.Comments.filter(approved=True)
    serializer = ProductSerializer(product)

    return render(
        request,
        'store/product_detail.html',
        {'product': product, 'approved_comments': approved_comments}
    )

# def post_detail(request, post_id):
#     post = get_object_or_404(Post, id=post_id)
#     # Filter and serialize only approved comments
#     approved_comments = post.comments.filter(approved=True)
#     serializer = PostSerializer(post)
#     return render(request, 'blog/post_detail.html', {'post': post, 'approved_comments': approved_comments})


def comment_view(request, product_id):
    if request.method == "Product":
        # Retrieve data from the form
        # author = request.user.id
        # comment_text = request.POST.get("comment", "")

        author = request.POST.get("author", "")
        comment_text = request.POST.get("comment", "")
        # Perform any necessary validation here

        # Create a new Comment instance and save it to the database
        comment = Comment(author_id=author, text=comment_text, product_id=product_id, approved=False)
        comment.save()

        comment = Comment(
            author_id=author, body=comment_text, product=Product.objects.get(id=product_id)
        )
        comment.save()

        # Redirect to a success page or the same page with a success message
        return redirect(reverse("product_detail", args=[product_id]))
    else:
        return redirect(reverse("product_detail", args=[product_id]))

        
    #     comment = Comment(
    #         author=author, body=comment_text, post=Post.objects.get(id=post_id)
    #     )
    #     comment.save()

    #     # Redirect to a success page or the same page with a success message
    #     return redirect(reverse("post_detail", args=[post_id]))
    # else:
    #     return redirect(reverse("post_detail", args=[post_id]))
# def comment_view(request, product_id):
#     if request.method == "POST":
#         # Retrieve data from the form
#         author = request.user.id  # Assuming you want to associate the comment with the logged-in user
#         comment_text = request.POST.get("text", "")

#         # Perform any necessary validation here

#         # Create a new Comment instance and save it to the database
#         comment = Comment(author_id=author, text=comment_text, product_id=product_id, approved=False)
#         comment.save()

#         # Redirect to a success page or the same page with a success message
#         return redirect(reverse("product_detail", args=[product_id]))
#     else:
#         return redirect(reverse("product_detail", args=[product_id]))

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
def api_product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    serializer = ProductSerializer(product)
    return Response(serializer.data)

    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def api_comment_list(request, product_id):
    if request.method == 'GET':
        comments = Comment.objects.filter(product_id=product_id, approved=True)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = {'author': request.user.id, 'product': product_id, 'text': request.data.get('text'), 'approved': False}
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return redirect('store:product_detail', product_id=product_id)
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
