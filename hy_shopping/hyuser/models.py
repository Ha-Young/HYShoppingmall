from django.db import models

# Create your models here.


class Hyuser(models.Model):
    email = models.EmailField(verbose_name='이메일')
    password = models.CharField(max_length=64, verbose_name='비밀번호')
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name='등록일')
    
    def __str__(self):
        return self.email


    class Meta:
        db_table = 'hyshop_hyuser'
        verbose_name = '사용자'
        verbose_name_plural = '사용자s'