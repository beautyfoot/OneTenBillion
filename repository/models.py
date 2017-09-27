from django.db import models

class League(models.Model):
    '''
    联赛
    '''
    l_name = models.CharField(max_length=32, verbose_name="联赛名")

    def __str__(self):
        return self.l_name

    class Meta:
        verbose_name = "联赛"
        verbose_name_plural = verbose_name


class Club(models.Model):
    '''
    俱乐部
    '''
    c_name = models.CharField(max_length=32, verbose_name="俱乐部名字")
    l_name = models.ForeignKey(League, verbose_name="所属联赛")

    def __str__(self):
        return self.c_name

    class Meta:
        verbose_name = "俱乐部"
        verbose_name_plural = verbose_name


class Play(models.Model):
    """
    比赛
    """
    results = (
        (0, "主队胜"),
        (1, "客队胜"),
        (2, "平局"),
    )

    z_name = models.ForeignKey(Club, verbose_name="主队", related_name="z_name_clubset")
    k_name = models.ForeignKey(Club, verbose_name="客队", related_name="k_name_clubset")
    p_time = models.DateTimeField(verbose_name="比赛时间")
    z_goal = models.SmallIntegerField(verbose_name="主队进球")
    k_goal = models.SmallIntegerField(verbose_name="客队进球")
    p_result = models.SmallIntegerField(choices=results, verbose_name="比赛结果")
    l_circle = models.IntegerField(max_length=2, verbose_name="比赛轮数")
    z_peilv = models.DecimalField(max_digits=5, decimal_places=3, verbose_name="主赔率")
    p_peilv = models.DecimalField(max_digits=5, decimal_places=3, verbose_name="平赔率")
    k_peilv = models.DecimalField(max_digits=5, decimal_places=3, verbose_name="客赔率")

    def __str__(self):
        return self.z_name.c_name + ":" + self.k_name.c_name

    class Meta:
        verbose_name = "比赛"
        verbose_name_plural = verbose_name


class PlayPosition(models.Model):
    """
    球员位置
    """
    position = models.CharField(max_length=32, verbose_name="位置")


class Player(models.Model):
    """
    球员
    """
    name = models.CharField(max_length=32, verbose_name="名字")
    c_name = models.ForeignKey(Club, verbose_name='俱乐部')
    position = models.ForeignKey(PlayPosition, verbose_name="位置", default=1)









