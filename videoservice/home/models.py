from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
# Create your models here.



def image_directory_path(instance, filename):
    return 'courses/{0}'.format( filename)


from django.contrib.auth import get_user_model

User = get_user_model()

SUBSCRIPTION = (
    ("F", "FREE"),
    ("m", "MONTHLY"),
    ("y", "YEARLY"),
)

class ProfileUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_pro = models.BooleanField(default=False)
    pro_expiry_date = models.DateTimeField(null=True, blank=True)
    subscription_type = models.CharField(max_length=100, choices=SUBSCRIPTION, default="FREE")

class Course(models.Model):
    course_name = models.CharField(max_length=200)
    course_description = RichTextField()
    is_premium = models.BooleanField(default=False)
    course_image = models.ImageField(upload_to = image_directory_path)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug =  slugify(self.course_name)
        super(Course, self).save(*args, **kwargs)


    def __str__(self):
        return self.course_name
    

class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_module_name=models.CharField(max_length=100)
    course_description = RichTextField()
    video_url = models.URLField(max_length=300)
    can_view = models.BooleanField(default=False)
