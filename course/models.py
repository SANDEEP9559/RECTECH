from django.db import models
from category.models import category
from django.urls import reverse

# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=200, unique=True)
    slug         = models.SlugField(max_length=200, unique=True)
    description  = models.TextField(max_length=500, blank=True)
    images       = models.ImageField(upload_to='photos/products')
    category     = models.ForeignKey(category, on_delete=models.CASCADE, null = True)
    def get_url(self):
        return reverse('course_detail', args=[self.category.slug, self.slug])

    def __str__(self):
        return self.course_name
