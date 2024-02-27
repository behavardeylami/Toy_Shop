from django.db import models

class BaseModel(models.Model):
    is_active = models.BooleanField(verbose_name="Is active", default=False)
    created_at = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name="Date updated", auto_now=True)
    
    
    class Meta:
        abstract = True
        ordering = ("pk",)


    def __str__(self):
        raise NotImplementedError("Implement __str__ method")