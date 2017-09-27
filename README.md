OneTenBillion
=====
这个文件是用来说明项目目标、注意事项和进展（更新）。
-----
# 目录
* 项目目标
* 注意事项

  * 关于静态文件
  * 关于视图函数
  * 关于url匹配
* 更新

项目目标
--------
### 初期
1. 自动采集联赛、俱乐部、球员、比赛及对应赔率信息
2. 生成各系列报表展示（前端展示）
3. 提供数据API接口，根据固定条件，提供赛事预测
   1. 提供个人条件设定，返回结果反馈
4. 注册、登陆

注意事项
---------
### 关于静态文件
所使用到的jQuery,Bootstrap直接使用<br>
    /static/js/jquery-3.2.1  和<br>
    /static/bootstrap/css/bootstrap.css<br>
    /static/bootstrap/js/bootstrap.js<br>
    /static/bootstrap/fonts/...<br>
    自己项目中需要使用到自定义css,js,img文件放到自己项目所在目录下的static相应目录中
### 关于视图函数
如果写CBV,class名字需有View后缀,比如
```python
class IndexView(View):
    pass
```
如果写FBV,def名字需有Func后缀,比如
```python
def indexFunc(request):
    pass
```
### 关于url匹配
自己的app下urls文件所写的url匹配需要写上name,如下所示
```python
urlpatterns = [
    url(r'^index/', IndexView.as_view(), name='index'),
]
```
如果不用View写视图函数,则使用
```python
urlpatterns = [
    url(r'^index/', indexFunc, name='index'),
]
```
如果需要用到url反向生成,<br>
  palyApp下的url需要前面加play前缀,比如 reverse('play:XXX')<br>
  clubApp下的url需要前面加play前缀,比如 reverse('club:XXX')<br>
  项目根目录下的url不需要前缀
