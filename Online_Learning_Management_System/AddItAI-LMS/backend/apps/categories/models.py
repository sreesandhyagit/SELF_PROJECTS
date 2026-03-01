from django.db import models
from django.utils.text import slugify


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150,unique=True)
    slug = models.SlugField(unique=True,blank=True)
    description = models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # prevent duplicate slug
    def generate_unique_slug(self):
        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1
        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug

    def save(self,*args,**kwargs):
        #auto generate slug
        if not self.slug:
            self.slug = self.generate_unique_slug()
        super().save(*args,**kwargs)

    def __str__(self):
        return self.name