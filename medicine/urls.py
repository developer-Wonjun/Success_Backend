from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings


app_name='medicine'

urlpatterns = [
    path('main/', main, name="main"),
    path('camera/', camera, name="camera"),
    path('blog/', blog, name="blog"),
    path('blog/<int:pk>/', posting, name="posting"),
    path('search', search, name='search'),
]


