from django.db import models
from intragram.users import models as user_model
# post를 표현하기 위한 모델 posts - 터미널에서 'django-admin startapp posts'를 입력

# Django data model을 만들 때 게시물 생성 날짜/업데이트 날짜를 Post/Comment마다 만들지 말고,
# TimeStampedModel에 상속 시켜주자
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class Post(TimeStampedModel):
    # 어떤 사람이 어떤 이미지와 캡션으로 포스트를 올렸는가? 누가 이 글을 좋아하는가?

    # Foreign key : https://brunch.co.kr/@dan-kim/26 설명 참조
    # 외부 테이블에서 참조해온 키
    author = models.ForeignKey(
            user_model.User, 
            null=True, 
            on_delete=models.CASCADE, # 외래키의 유저가 삭제되면 같이 삭제됨
            related_name='post_author'    
        )
    image = models.ImageField(blank=True)
    caption = models.TextField(blank=True)
    
    # 여러 유저가 포스트를 좋아할 수 있으므로, 다대다 구조
    image_likes = models.ManyToManyField(
                user_model.User,
                related_name ='post_image_like'
            )
    


class Comment(TimeStampedModel):
    # 어떤 사람이 어떤 포스트에 어떤 내용의 코멘트를 썼는가?
    author = models.ForeignKey(
            user_model.User, 
            null=True, 
            on_delete=models.CASCADE, # 외래키의 유저가 삭제되면 같이 삭제됨
            related_name='comment_author'    
        )
    posts = models.ForeignKey(
            Post,
            null=True,
            on_delete=models.CASCADE,
            related_name='comment_post'
        )
    contents = models.TextField(blank=True)