from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from cart.models import ShoppingBasket, BasketItem
from .models import Category, Product, Comment
from .serializers import CategorySerializer, ProductSerializer, CommentSerializer
from .forms import CommentForm

# Template Views
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'store/category_list.html', {'categories': categories})


def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'store/category_detail.html', {'category': category})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    approved_comments = product.Comments.filter(approved=True)

    # Get the user's shopping basket
    if request.user.is_authenticated:
        user_basket, created = ShoppingBasket.objects.get_or_create(user=request.user)
        basket_items = BasketItem.objects.filter(order=user_basket)
    else:
        user_basket = None
        basket_items = []

    context = {
        # 'price': price,
        'product': product,
        'approved_comments': approved_comments,
        'user_basket': user_basket,
        'basket_items': basket_items,
        'total_price': user_basket.total_price,
    }

    return render(request, 'store/product_detail.html', context)

    # product = get_object_or_404(Product, id=product_id)
    # basket_items = BasketItem.objects.filter(order=request.user.shoppingbasket)
    # context = {
    #     'product': product,
    #     'approved_comments': product.Comments.filter(approved=True),
    #     'user_basket': request.user.shoppingbasket,
    #     'basket_items': basket_items,
    # }
    # # Filter and serialize only approved comments
    # # approved_comments = product.Comments.filter(approved=True)
    # # serializer = ProductSerializer(product)

    # return render(request, 'store/product_detail.html', context)

    # # return render(
    # #     request,
    # #     'store/product_detail.html',
    # #     {'product': product, 'approved_comments': approved_comments}
    # # )


def comment_view(request, product_id):
    if request.method == "Product":

        author = request.POST.get("author", "")
        comment_text = request.POST.get("comment", "")

        comment = Comment(author_id=author, text=comment_text, product_id=product_id, approved=False)
        comment.save()

        comment = Comment(
            author_id=author, body=comment_text, product=Product.objects.get(id=product_id)
        )
        comment.save()

        return redirect(reverse("product_detail", args=[product_id]))
    else:
        return redirect(reverse("product_detail", args=[product_id]))


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


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Get or create the user's shopping basket
    user_basket, created = ShoppingBasket.objects.get_or_create(user=request.user)

    # Get or create the basket item for the product in the basket
    basket_item, created = BasketItem.objects.get_or_create(order=user_basket, product=product)

    # Increment the quantity of the basket item
    basket_item.quantity += 1
    basket_item.save()

    user_basket.update_total_price()

    # Redirect back to the product detail page
    return redirect('store:product_detail', product_id=product_id)