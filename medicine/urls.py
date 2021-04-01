from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings


app_name='medicine'

urlpatterns = [
    path('blog/', blog, name="blog"),
    path('blog/<int:pk>/', posting, name="posting"),
]


