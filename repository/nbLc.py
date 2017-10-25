from nb_lc.service import nb
from nb_lc.service.nb import Option
from . import models


class PlayConfig(nb.ModelNb):
    def result(self, obj=None, is_header=False):
        """
        显示比赛结果choices中中文信息
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return "比赛结果"
        return obj.get_p_result_display  # 显示choices的方式

    list_display = ["p_time", "z_name", "k_name", result, "l_circle", "z_peilv", "p_peilv", "k_peilv", ]
    list_filter = [
        Option("z_name", "", lambda x: x.c_name, lambda x: x.c_name,),
        Option("k_name", True, lambda x: x.c_name, lambda x: x.c_name,)
    ]


nb.site.register(models.Play, PlayConfig)

nb.site.register(models.PlayPosition)
nb.site.register(models.Player)
nb.site.register(models.League)
nb.site.register(models.Club)
