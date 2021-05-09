from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from django.utils import timezone
from .form import BlogUpdate

def index(request):
    return render(request, 'index.html')
# Create your views here.

def start(request):
    return render(request, 'start.html')


def home(request):
    blogs = Blog.objects.order_by('-id')
    return render(request, 'home.html', {'blogs': blogs})

def detail(request, blog_id):
    blog_detail = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'detail.html', {'blog': blog_detail})
def create(request):
    return render(request, 'create.html')

def postcreate(request):
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save()
    return redirect('/main/community/' + str(blog.id))
    
def new(request):
    full_text = request.GET['fulltext']

    word_list = full_text.split()

    word_dictionary = {}

    for word in word_list:
        if word in word_dictionary:
            # Increase
            word_dictionary[word] += 1
        else:
            # add to the dictionary
            word_dictionary[word] = 1

    return render(request, 'new.html', {'fulltext': full_text, 'total': len(word_list), 'dictionary': word_dictionary.items()} )


def update(request, blog_id):
    blog = Blog.objects.get(id=blog_id)

    if request.method == "POST":
        form = BlogUpdate(request.POST)
        if form.is_valid():
            blog.title = form.cleaned_data['title']
            blog.body = form.cleaned_data['body']
            blog.pub_date = timezone.datetime.now()
            blog.save()
            return redirect('/main/community/' + str(blog.id))

    else:
        form = BlogUpdate(instance = blog)
        return render(request, 'update.html', {'form':form}) 

def delete(request, blog_id):
    blog = Blog.objects.get(id=blog_id)
    blog.delete()
    return redirect('/main/community/')


def alarm(request):
    return render(request, 'alarm.html')

def map(request):
    return render(request, 'map.html')

