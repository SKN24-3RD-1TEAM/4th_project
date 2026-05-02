from django.db import models

class User(models.Model):
    # 필드 정의 (예: 이름, 이메일 등)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username