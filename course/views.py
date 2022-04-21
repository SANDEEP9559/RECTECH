from django.shortcuts import render, get_object_or_404
from .models import Course
from category.models import category

# Create your views here.
def course(request, category_slug=None):
    categories = None
    course = None
    if category_slug != None:
        categories = get_object_or_404(category, slug=category_slug)
        course = Course.objects.filter(category=categories)

    else:
        course = Course.objects.all()
        
    context = {
         'course': course,

    }
    return render(request, 'course/course.html',context)



def course_detail(request, category_slug, course_slug):
    try:
        single_course = Course.objects.get(category__slug=category_slug, slug=course_slug)
    except Exception as e:
        raise e


    context = {
      'single_product': single_course,

    }
    return render(request, 'course/course_detail.html', context)
