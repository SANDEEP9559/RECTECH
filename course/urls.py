from django.urls import path
from .import views

urlpatterns = [
   path('',views.course ,name='course'),
   path('<slug:category_slug>/',views.course, name='course_by_category'),
   path('<slug:category_slug>/<slug:course_slug>/',views.course_detail, name='course_detail'),
]
