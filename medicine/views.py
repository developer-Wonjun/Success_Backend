from django.shortcuts import render
# View에 Model(Post 게시글) 가져오기
from .models import Post, Photo
from django.core.paginator import Paginator
from django.views.generic import CreateView
# index.html 페이지를 부르는 index 함수

# blog.html 페이지를 부르는 blog 함수

def main(request):
    return render(request, 'medicine/main.html')

def camera(request):
    return render(request, 'medicine/camera.html')

def blog(request):
    # 모든 Post를 가져와 postlist에 저장합니다
    postlist = Post.objects.order_by('-id')
    post = Post.objects.all().order_by('-id')
    paginator = Paginator(post,3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    # blog.html 페이지를 열 때, 모든 Post인 postlist도 같이 가져옵니다 
    return render(request, 'medicine/blog.html', {'postlist':postlist, 'posts':posts})

def posting(request, pk):
    # 게시글(Post) 중 pk(primary_key)를 이용해 하나의 게시글(post)를 검색
    post = Post.objects.get(pk=pk)
    # posting.html 페이지를 열 때, 찾아낸 게시글(post)을 post라는 이름으로 가져옴
    return render(request, 'medicine/posting.html', {'post':post})


def search(request):
    postlist = Post.objects.all().order_by('-id')

    q = request.POST.get('q', "") 

    if q:
        postlist = postlist.filter(postname__icontains=q)
        return render(request, 'medicine/search.html', {'postlist' : postlist, 'q' : q})
    
    else:
        return render(request, 'medicine/search.html')


def InsertPhoto(request):
    form=Photo()
    form.photo=request.FILES['image']
    form.save()

    return render(request, 'medicine/main.html')   