from django.db import models
from user.models import BaseModel
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class Category(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name="Name", unique=True)
    description = models.TextField(null=False, blank=False, verbose_name="Description")

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('name', )


    def __str__(self):
        return self.name
    

class Post(BaseModel):
    title = models.CharField(max_length=255, null=False, blank=False, verbose_name='Title')
    body = models.TextField(null=False, blank=False, verbose_name='Body')
    category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(UserModel, on_delete=models.PROTECT, verbose_name='Author', related_name='posts')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date')

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return self.title


class Media(BaseModel):
    MEDIA_TYPE = (
        ("image", "Image"),
        ("video", "Video"),
        ("audio", "Audio"),
    )

    file = models.FileField(upload_to='blog/media/', verbose_name='File')
    media_type = models.CharField(
        max_length=10, 
        choices=MEDIA_TYPE, 
        default="image", 
        null=False, 
        blank=False,
        verbose_name='Media type'
        )
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post', related_name='Medias')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Media'
        verbose_name_plural = 'Medias'

    def __str__(self):
        return self.title
    

class Comment(BaseModel):
    author = models.ForeignKey(UserModel, on_delete=models.PROTECT, verbose_name='User', related_name='Posts')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Post', related_name='comments')
    text = models.TextField(null=False, blank=False, verbose_name='Comment')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date')
    approved = models.BooleanField(default=False, verbose_name='Approved')


    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'{self.author.username} - {self.text}'
