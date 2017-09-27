from django.db import models
from clubApp.models import Club


class Play(models.Model):

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
    l_circle = models.SmallIntegerField(verbose_name="比赛轮数")
    z_peilv = models.DecimalField(max_digits=5, decimal_places=3, verbose_name="主赔率")
    p_peilv = models.DecimalField(max_digits=5, decimal_places=3, verbose_name="平赔率")
    k_peilv = models.DecimalField(max_digits=5, decimal_places=3, verbose_name="客赔率")


    def __str__(self):
        return self.z_name.c_name + ":" + self.k_name.c_name

    class Meta:
        verbose_name = "比赛"
        verbose_name_plural = verbose_name
