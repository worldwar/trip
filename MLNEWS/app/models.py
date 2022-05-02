from django.db import models
# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128,verbose_name='用户名')
    tel = models.CharField(max_length=128,verbose_name='手机')
    password = models.CharField(max_length=128,verbose_name='密码')
    class Meta:
        verbose_name_plural = '用户表'  # 此时，admin中表的名字就是‘用户表‘
    def __str__(self):
        return self.name








class JingQu(models.Model):
    id = models.AutoField(primary_key=True)
    sheng = models.CharField(max_length=32)
    sheng_url = models.CharField(max_length=128)

    city = models.CharField(max_length=32)
    city_url =  models.CharField(max_length=128)

    jingqu = models.CharField(max_length=32)
    jingqu_url =  models.CharField(max_length=128)

    ever = models.IntegerField()
    never = models.IntegerField()
    level = models.CharField(max_length=32,null=True)

    img =  models.CharField(max_length=128,default='')
    class Meta:
        verbose_name_plural = '景区表'  # 此时，admin中表的名字就是‘浏览‘


class JingDian(models.Model):
    id = models.AutoField(primary_key=True)
    jingqu = models.ForeignKey(JingQu,verbose_name='景区的外键',on_delete=models.CASCADE)
    detail = models.CharField(max_length=256)
    img =  models.CharField(max_length=256,default='')
    title = models.CharField(max_length=64)
    def __str__(self):
        return self.title

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='用户名')
    time = models.DateTimeField(auto_now=True,verbose_name='评论时间')
    jingdian = models.ForeignKey(JingDian,on_delete=models.CASCADE,verbose_name='景点')
    content = models.CharField(max_length=256,verbose_name='内容')
    score = models.IntegerField(verbose_name='评分') # 评分


class Like(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User,models.CASCADE)
    jingqu = models.ForeignKey(JingQu,models.CASCADE)
    class Meta:
        verbose_name_plural = '收藏'  # 此时，admin中表的名字就是‘用户表‘


class See(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.ForeignKey(User, models.CASCADE)
    jingqu = models.ForeignKey(JingQu, models.CASCADE)
    num = models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = '浏览表'  # 此时，admin中表的名字就是‘浏览‘

class Sight(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    desc = models.TextField()
    city = models.CharField(max_length=128)
    level = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    price = models.FloatField()
    sales = models.IntegerField()
    hot = models.FloatField()
    comment_high = models.IntegerField(default=0, verbose_name='好评')
    comment_mid = models.IntegerField(default=0, verbose_name='中评')
    comment_low = models.IntegerField(default=0, verbose_name='差评')
    comments = models.IntegerField(default=0, verbose_name='全部')
    comment_mark = models.CharField(max_length=128)
    class Meta:
        db_table = 'sight'
        verbose_name_plural = '景点表'
Sight.objects = Sight.objects.using('qunar')

class Restaurant(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    desc = models.TextField()
    city = models.CharField(max_length=128)
    address = models.TextField()
    score = models.FloatField()
    comments = models.IntegerField(default=0, verbose_name='评论数')
    class Meta:
        db_table = 'restaurant'
        verbose_name_plural = '餐厅表'
Restaurant.objects = Restaurant.objects.using('qunar')





