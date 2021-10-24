from django.shortcuts import render

# View에 Model(Post 게시글) 가져오기
from .models import Post, Photo
from django.core.paginator import Paginator
from django.views.generic import CreateView
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.shortcuts import get_object_or_404
from tensorflow.keras.models import load_model
import tensorflow as tf
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt
import glob
import os.path
import requests
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

    return redirect('medicine:result') 

def result(request):
# resize, mask 
    # if os.path.isfile(r'media/images/**/*.jpg'):
    if glob.glob('media/images/*.jpg'):

        root = r'media/images/*.jpg'
    else:
        root = r'media/images/*.png'
    # elif os.path.isfile(r'media/images/**/*.png'):
    #     root = r'media/images/*.png'
    # else:
    #     root = '존재안함'
    path = glob.glob(str(root))
    img1 = path[0]   
    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        files={'image_file': open(img1, 'rb')},
        data={'size': 'auto'},
        headers={'X-Api-Key': 'ptCZx3qrSXY86os3MGCVPUe8'},
    )
    if response.status_code == requests.codes.ok:
        with open('media/images/0.png', 'wb') as out:
            out.write(response.content)
    else:
        print("Error:", response.status_code, response.text)
    img2 = r'media/images/0.png'

    img3 = cv2.imread(img2)

# resize        
    resize_img = cv2.resize(img3,dsize=(67,67),interpolation=cv2.INTER_AREA)
    cv2.imwrite('media/images/1.png', resize_img)
# np.list
    mat = glob.glob('media/images/1.png')
    img = cv2.imread(mat[0])
    arr = np.array(img)
    list_x = []
    list_x.append(arr)
    result = np.array(list_x)
#load model
    model = load_model('jong_s_pill_last_s91.h5')
    predictions = model.predict(result)
    rs = np.argmax(predictions)

    post = Post.objects.filter(id=rs)

    [os.remove(f) for f in glob.glob(str(root))]

    return render(request, "medicine/result.html", {'rs':rs, 'post':post})