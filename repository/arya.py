from django.db.models import Q

from arya.service.sites import site, AryaConfig, FilterOption
from . import models

site.register(models.League)


class ClubConfig(AryaConfig):
    list_display = ['c_name', 'l_name']

    list_filter = [
        FilterOption('l_name', True, ),
        FilterOption('c_name', True, lambda x: x.c_name, lambda x: x.c_name)
    ]


site.register(models.Club, ClubConfig)


class PlayConfig(AryaConfig):
    def all_goal(self, obj=None, is_header=False):
        """
        定制显示函数
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return "总进球数"
        count_goal = int(obj.z_goal) + int(obj.k_goal)
        return count_goal

    def p_result_display(self, obj=None, is_header=False):
        """
        choices关系，显示方式
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return "比赛结果"
        return obj.get_p_result_display()

    list_display = ['l_circle', 'z_name', 'k_name', 'z_goal', 'k_goal', all_goal, p_result_display, 'z_peilv',
                    'p_peilv', 'k_peilv']

    list_filter = [
        # FilterOption('z_name', conditon=Q(l_name_id=2), ),  # LB,强制显示同一个联赛的球队名字
        FilterOption('z_name', is_multi=True),  # LB,强制显示同一个联赛的球队名字
        FilterOption('k_name', is_multi=True),
        # FilterOption('p_result', True, lambda x:x.get_p_result_display(), lambda x: x.p_result),
        FilterOption('p_result'),  # choices选择项
    ]


site.register(models.Play, PlayConfig)

site.register(models.Player)

site.register(models.PlayPosition)
