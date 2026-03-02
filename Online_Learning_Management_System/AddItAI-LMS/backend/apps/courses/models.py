from django.db import models
from django.utils.text import slugify
from apps.accounts.models import User
from apps.categories.models import Category


# Create your models here.

class Course(models.Model):

    class Level(models.TextChoices):
        ALL = "ALL","All Levels"
        BEGINNER = "BEGINNER","Beginner"
        INTERMEDIATE = "INTERMEDIATE","Intermediate"
        ADVANCED = "ADVANCED","Advanced"

    class Status(models.TextChoices):
        DRAFT = "DRAFT","Draft"
        PENDING = "PENDING","Pending Approval"
        APPROVED = "APPROVED","Approved"
        REJECTED = "REJECTED","Rejected"

    class CourseType(models.TextChoices):
        FREE = "free","Free"
        PAID = "paid","Paid"
        CERTIFICATION="certification","Certification"

        
    instructor = models.ForeignKey(User,on_delete=models.CASCADE, related_name="courses")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="courses")
    
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,blank=True)

    description = models.TextField()
    thumbnail = models.ImageField(upload_to="courses/",blank=True,null=True)

    course_type=models.CharField(max_length=20, choices=CourseType.choices,default=CourseType.FREE)
    price = models.DecimalField(max_digits=8,decimal_places=2,default=0.00)

    duration = models.IntegerField(help_text="Duration in Minutes",default=0)
    level = models.CharField(max_length=20,choices=Level.choices,default=Level.BEGINNER)

    language = models.CharField(max_length=50,default="English")
    preview_video = models.URLField(blank=True,null=True)
    
    is_published = models.BooleanField(default=False)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.DRAFT)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self,*args,**kwargs):
        #auto assign course type
        if self.price ==0:
            self.course_type="free"
        elif self.course_type != "certification":
            self.course_type = "paid"            
        #generate unique slug 
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Course.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug =slug        
        super().save(*args,**kwargs)
    
    def __str__(self):
        return self.title
    
    @property
    def is_free(self):
        return self.course_type == "free"
    
    
    

