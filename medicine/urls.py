from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings


app_name='medicine'

urlpatterns = [
    path('main/', main, name="main"),
    path('blog/', blog, name="blog"),
    path('blog/<int:pk>/', posting, name="posting"),
    path('search', search, name='search'),

    path('insert/', InsertPhoto, name='insert')
] 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


