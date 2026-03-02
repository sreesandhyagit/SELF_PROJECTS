from django.db import models
from django.utils.text import slugify
import re


class Section(models.Model):
    course = models.ForeignKey("courses.Course",on_delete=models.CASCADE,related_name="sections")
    title=models.CharField(max_length=255)
    slug=models.SlugField(unique=True,blank=True)
    order=models.PositiveIntegerField(default=0)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=["order"]

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super().save(*args,**kwargs)

    def __str__(self):
        return self.title


def extract_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]+)",url)
    return match.group(1) if match else None

#----------------------------------------------------------------------------------------------------------

class Lesson(models.Model):
    section =models.ForeignKey("lessons.Section",on_delete=models.CASCADE,related_name="lessons")
    title=models.CharField(max_length=255)
    slug=models.SlugField(unique=True,blank=True)
    youtube_url=models.URLField()
    duration=models.PositiveIntegerField(help_text="Enter duration in seconds (auto converted from HH:MM:SS)")
    thumbnail=models.URLField(null=True,blank=True)
    order=models.PositiveBigIntegerField(default=0)
    is_preview=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=["order"]

    def get_duration_display(self):
        duration=self.duration or 0
        hours=duration // 3600
        minutes=(duration % 3600) // 60
        seconds=duration % 60
        return f"{hours}:{minutes:02}:{seconds:02}"
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug=slugify(self.title)

        if self.youtube_url:
            video_id=extract_video_id(self.youtube_url)
            if video_id and not self.thumbnail:
                self.thumbnail=f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
            
        super().save(*args,**kwargs)

    def __str__(self):
        return self.title
    
#-------------------------------------------------------------------------------------------------------------


    
    

