from django.db import models

# Create your models here.
class Course(models.Model):
    course_name=models.CharField(max_length=100)
    duration=models.CharField(max_length=50)
    fee=models.DecimalField(max_digits=8,decimal_places=2)

    def __str__(self):
        return self.course_name

class Teacher(models.Model):
    teacher_image=models.ImageField(upload_to="teachers/",default="teachers/default_profile_image.jpg")
    teacher_name=models.CharField(max_length=100)
    teacher_phone=models.CharField(max_length=15,blank=True,null=True)
    teacher_email=models.EmailField(unique=True,blank=True,null=True)     
    courses=models.ManyToManyField(Course,blank=True)

    def __str__(self):
        return self.teacher_name

class Batch(models.Model):
    batch_name=models.CharField(max_length=50)
    start_date=models.DateField()
    course=models.ForeignKey(Course,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.batch_name} - {self.course.course_name}"

class Student(models.Model):
    PLATFORM_CHOICES = (
        ('online','Online'),
        ('offline','Offline')
    )
    student_name=models.CharField(max_length=100)
    student_email=models.EmailField(unique=True,blank=True,null=True)
    student_phone=models.CharField(max_length=15,blank=True,null=True)
    student_image=models.ImageField(upload_to='students/',default="students/default_profile_image.jpg")
    platform=models.CharField(max_length=10,choices=PLATFORM_CHOICES)

    def __str__(self):
        return self.student_name
    
class Enrollment(models.Model):
    student=models.ForeignKey(Student,on_delete=models.CASCADE)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    batch=models.ForeignKey(Batch,on_delete=models.CASCADE)
    joined_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.student_name} - {self.course.course_name}"