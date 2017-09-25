版本更新：
V7.2
1、添加playApp字段查询渲染（jzh）
V7.1
1、增加userApp（用户）
2、增加dateApp（数据爬取）
且都已添加settings设置
V7.0
1、增加playerApp（球员）
2、修改playApp字段l_circle，为数字代表轮数


关于静态文件:
    所使用到的jQuery,Bootstrap直接使用
    /static/js/jquery-3.2.1  和
    /static/bootstrap/css/bootstrap.css
    /static/bootstrap/js/bootstrap.js
    /static/bootstrap/fonts/...

    自己项目中需要使用到自定义css,js,img文件放到自己项目所在目录下的static相应目录中



关于视图函数:

    如果写CBV,class名字需有View后缀,比如
    class IndexView(View):

    如果写FBV,def名字需有Func后缀,比如
    def indexFunc(request):


关于url匹配:

    自己的app下urls文件所写的url匹配需要写上name,如下所示
    urlpatterns = [
        url(r'^index/', IndexView.as_view(), name='index'),
    ]

    如果不用View写视图函数,则使用
    urlpatterns = [
        url(r'^index/', indexFunc, name='index'),
    ]

    如果需要用到url反向生成,
    palyApp下的url需要前面加play前缀,比如 reverse('play:XXX')
    clubApp下的url需要前面加play前缀,比如 reverse('club:XXX')
    项目根目录下的url不需要前缀
