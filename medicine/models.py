from django.db import models

class Post(models.Model):
    postname = models.CharField(max_length=50)
    # 게시글 Post에 이미지 추가
    mainphoto = models.ImageField(blank=True, null=True)
    company = models.CharField(max_length=100) # 제조사
    efficacy = models.CharField(max_length=100) # 효능
    way = models.CharField(max_length=100) # 복용 방법
    precautions = models.CharField(max_length=100) #주의사항 


    # postname이 Post object 대신 나오기
    def __str__(self):
        return self.postname