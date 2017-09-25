from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from playApp.models import Play
from clubApp.models import League, Club


class IndexView(View):
    def get(self, request):
        return HttpResponse('Hello Football')


class LeaguesView(View):
    '''
    lgs：联赛列表
    '''

    def get(self, request):
        lgs = League.objects.all()
        return render(request, 'index.html', {'leagues': lgs})


class RoundView(View):
    '''
    league_num 联赛id
    round_num 第几轮
    '''

    def get(self, request, league_num=1, round_num=1):
        # ******应该有个查询是哪个联赛的步骤***********
        # print(league_num)
        # print(round_num)
        all_play = Play.objects.all()
        rund = all_play.values('l_circle').distinct()
        play_table = all_play.filter(l_circle=round_num)
        return render(request, 'Round.html', {'league':league_num,'round': rund, 'table': play_table})
