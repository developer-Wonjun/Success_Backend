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
    if glob.glob('media/images/*.jpg').exists():

        root = r'media/images/*.jpg'
    else:
        root = r'media/images/*.PNG'
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
        with open(str(root), 'wb') as out:
            out.write(response.content)
    else:
        print("Error:", response.status_code, response.text)

    path2 =(str(root))
    img = cv2.imread(path2)

    path = glob.glob(str(root))
    img1 = path[0]
    img = cv2.imread(img1)
    img = cv2.resize(img,dsize=(676,369),interpolation=cv2.INTER_AREA)
    mask = np.zeros(img.shape[:2], np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    rect = (0,0,700,350)
    cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
    mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
    img = img*mask2[:,:,np.newaxis]
# boundingbox  
    small = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    grad = cv2.morphologyEx(small, cv2.MORPH_GRADIENT, kernel)
    _, bw = cv2.threshold(grad, 0.0, 255.0, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 1))
    connected = cv2.morphologyEx(bw, cv2.MORPH_CLOSE, kernel)
    contours, hierarchy = cv2.findContours(connected.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    mask = np.zeros(bw.shape, dtype=np.uint8)
    for idx in range(len(contours)):
        x, y, w, h = cv2.boundingRect(contours[idx])
        mask[y:y+h, x:x+w] = 0
        cv2.drawContours(mask, contours, idx, (255, 255, 255), -1)
        r = float(cv2.countNonZero(mask[y:y+h, x:x+w])) / (w * h)
        if r > 0.45 and w > 8 and h > 8:
            cv2.rectangle(img, (x, y), (x+w-1, y+h-1), (0, 255, 0), 2) 
# canny        
    edge = cv2.Canny(img, 50, 250) 
    resize_edge = cv2.resize(edge,dsize=(68,37),interpolation=cv2.INTER_AREA)
    cv2.imwrite(str(root), resize_edge)
# np.list
    mat = glob.glob(str(root))
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
