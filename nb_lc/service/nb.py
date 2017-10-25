import copy

from django.forms import ModelForm
from django.http import QueryDict
from django.shortcuts import HttpResponse, render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe
from types import FunctionType

from utils.page import Pagination


class RowItems(object):
    """
    组合搜索项
    """

    def __init__(self, option, change_list, data_list, params=None):
        self.option = option
        self.change_list = change_list
        self.data_list = data_list
        self.params = copy.deepcopy(params)
        self.params._mutable = True  # 配置此项，才可以修改request

    def __iter__(self):
        base_url = self.change_list.model_config_obj.reverse_change_list_url()
        tpl = "<a href='{0}' class='{1}'>{2}</a>"
        # print(base_url)
        # print(self.params)               <QueryDict: {'group': ['1', '2']}>
        # print(self.params.urlencode())   group=1&group=2
        if self.option.name in self.params:
            pop_value = self.params.pop(self.option.name)
            url = "{0}?{1}".format(base_url, self.params.urlencode())
            val = tpl.format(url, "", "全部", )
            self.params.setlist(self.option.name, pop_value)
        else:
            url = "{0}?{1}".format(base_url, self.params.urlencode())
            val = tpl.format(url, "active", "全部", )
        yield mark_safe("<div class='whole'>")
        yield mark_safe(val)
        yield mark_safe("</div>")

        yield mark_safe("<div class='others'>")
        for obj in self.data_list:

            # 自定制：显示名字和传参
            pk = self.option.val_func_name(obj) if self.option.val_func_name else obj.pk
            pk = str(pk)
            text = self.option.text_func_name(obj) if self.option.text_func_name else str(obj)

            params = copy.deepcopy(self.params)  # request复制一定要使用copy.deepcopy()

            exist = False
            if pk in params.getlist(self.option.name):  # pk已存在
                exist = True

            if self.option.is_multi:  # 是多选
                if exist:
                    values = params.getlist(self.option.name)
                    values.remove(pk)
                    params.setlist(self.option.name, values)
                else:
                    params.appendlist(self.option.name, pk)
            else:
                if exist:
                    params.pop(self.option.name)  # 单选模式，再次点击去掉选择
                    # params[self.option.name] = pop_value
                else:
                    params[self.option.name] = pk  # request里设置值，一遍urlencode（）转换url
            url = "{0}?{1}".format(base_url, params.urlencode())

            if exist:
                # params.getlist(self.option.name).remove(pk)
                val = tpl.format(url, "active", text, )
            else:
                val = tpl.format(url, "", text, )
            yield mark_safe(val)
        yield mark_safe("</div>")


class Option(object):
    def __init__(self, name_or_func, is_multi=False, text_func_name=None, val_func_name=None):
        """
        配置四个参数，助于显示filter_list
        :param name_or_func: 字段名，或者函数名字
        :param is_multi: 是否可以多选（默认单选）
        :param text_func_name: 页面显示字段信息，默认使用str(对象)
        :param val_func_name: url传值信息，默认使用 obj.pk
        """
        self.name_or_func = name_or_func
        self.is_multi = is_multi
        self.text_func_name = text_func_name
        self.val_func_name = val_func_name

    @property
    def is_func(self):
        if isinstance(self.name_or_func, FunctionType):
            return True

    @property
    def name(self):
        if self.is_func:
            return self.name_or_func.__name__
        else:
            return self.name_or_func


class ChangeList(object):
    def __init__(self, data_list, model_config_obj):
        self.list_display = model_config_obj.get_list_display()
        self.actions = model_config_obj.get_actions()
        self.list_filter = model_config_obj.get_list_filter()

        self.model_config_obj = model_config_obj

        """ 分页开始 """
        request_get = copy.deepcopy(model_config_obj.request.GET)
        request_get._mutable = True
        # print(request_get)
        request_get['page'] = 9
        # print(request_get.urlencode())

        page = Pagination(
            current_page=model_config_obj.request.GET.get('page'),
            total_item_count=data_list.count(),
            base_url=model_config_obj.request.path_info,
            request_params=request_get
        )

        self.data_list = data_list[page.start:page.end]
        self.page_html = page.page_html()
        """ 分页结束 """

    def add_html(self):
        """
        添加按钮
        :return:
        """
        app_model = self.model_config_obj.model_class._meta.app_label, self.model_config_obj.model_class._meta.model_name
        add_url = reverse("nb:%s_%s_add" % app_model)
        query_dict = QueryDict(mutable=True)
        query_dict['_xxxxxxxxxxxx'] = self.model_config_obj.request.GET.urlencode()

        add_html = mark_safe('<a class="btn btn-primary" href="%s?%s">添加</a>' % (add_url, query_dict.urlencode(),))
        return add_html

    def get_list_filter(self):
        model_class = self.model_config_obj.model_class  # UserInfo类
        for option in self.list_filter:  # [Option, Option]
            # 当前操作的表
            from django.db.models.fields.related import RelatedField
            field_obj = model_class._meta.get_field(option.name)  # 获得字符串对应表对象

            if isinstance(field_obj, RelatedField):
                field_related_class = field_obj.rel.to  # 通过关系字符获得关系表对象（FK，MM）
                data_list = field_related_class.objects.all()
                data_list = RowItems(option, self, data_list, self.model_config_obj.request.GET)
            else:
                data_list = model_class.objects.all()
                data_list = RowItems(option, self, data_list, self.model_config_obj.request.GET)

            yield data_list  # [obj,obj,obj]

            # model_class = self.model_config_obj.model_class  # UserInfo类
            # for name in self.list_filter:  # ['group','roles']
            #     # 当前操作的表
            #     from django.db.models.fields.related import RelatedField
            #     field_obj = model_class._meta.get_field(name)
            #
            #     if isinstance(field_obj, RelatedField):
            #         field_related_class = field_obj.rel.to
            #         # data_list = Foo(field_related_class.objects.all())
            #         data_list = field_related_class.objects.all()
            #     else:
            #         # data_list = Foo(model_class.objects.all())
            #         data_list = model_class.objects.all()
            #
            #     yield data_list  # [obj,obj,obj]


class ModelNb(object):
    """
    基础配置类
    """
    list_display = []

    # 默认选择和按钮显示
    def choose(self, obj=None, is_header=False):
        if is_header:
            return "选择"
        else:
            tpl = "<input type='checkbox' value='%s' />" % (obj.pk,)
            return mark_safe(tpl)

    def option(self, obj=None, is_header=False):
        if is_header:
            return "功能选项"
        else:
            edit_url = reverse(
                "nb:%s_%s_change" % (self.model_class._meta.app_label, self.model_class._meta.model_name),
                args=(obj.pk,))
            delete_url = reverse(
                "nb:%s_%s_delete" % (self.model_class._meta.app_label, self.model_class._meta.model_name),
                args=(obj.pk,))
            tpl = "<a href='%s'>编辑</a>|<a href='%s'>删除</a>" % (edit_url, delete_url,)
            return mark_safe(tpl)

    def get_list_display(self):
        """
        list_diaplay显示
        :return:
        """
        result_list = []
        if self.list_display:
            result_list.extend(self.list_display)
            result_list.insert(0, ModelNb.choose)
            result_list.append(ModelNb.option)
        return result_list

    show_add_btn = True

    def get_show_add_btn(self):
        return self.show_add_btn

    def __init__(self, model_class, site):
        self.model_class = model_class  # 类名
        self.site = site

        self.app_label = model_class._meta.app_label
        self.model_name = model_class._meta.model_name

        self.request = None

        self.change_filter_name = "_change_filter"

    """定制action"""
    actions = []

    def multi_del(self):
        pk_list = self.request.POST.getlist('pk')
        # self.model_class.objects.filter(pk__in=pk_list).delete()

    multi_del.short_desc = "批量删除"  # 中文显示名字

    def init_action(self):
        pass

    init_action.short_desc = "初始化"

    def get_actions(self):
        result = []
        result.extend(self.actions)
        result.append(ModelNb.multi_del)
        result.append(ModelNb.init_action)
        return result
    """定制action"""

    """ 定制modleform """
    model_form = None

    def get_model_form_class(self):
        result = self.model_form
        if not result:
            class DefaultModelForm(ModelForm):
                class Meta:
                    model = self.model_class
                    fields = "__all__"

            result = DefaultModelForm
        return result

    """ 结束modelForm """

    """ 定制组合筛选 """
    list_filter = []

    def get_list_filter(self):
        return self.list_filter

    """ 结束组合筛选 """

    def changelist_view(self, request, *args, **kwargs):
        self.request = request

        if request.method == "POST":
            action_name = request.POST.get('action')
            action_method = getattr(self, action_name, None)
            if action_method:
                action_method()

        data_list = self.model_class.objects.all()

        # def headers():
        #     """
        #     定制表头内容
        #     :return:
        #     """
        #     if not self.list_display:
        #         yield self.model_class._meta.model_name
        #     else:
        #         for v in self.list_display:
        #             yield v(self, is_header=True) if isinstance(v, FunctionType) else self.model_class._meta.get_field(v).verbose_name
        #
        # def body():
        #     for row in data_list:
        #         if not self.list_display:
        #             yield [str(row),]  # ?
        #         else:
        #             yield [name(self, obj=row) if isinstance(name, FunctionType) else getattr(row, name) for name in self.list_display]

        cl = ChangeList(data_list, self)
        # add_url = reverse('nb:%s_%s_add' %(self.model_class._meta.app_label,self.model_class._meta.model_name,))
        content = {
            "cl": cl,
        }

        return render(request, "nb_lc/changelist.html", content)
        # return HttpResponse('列表页面')

    def add_view(self, request, *args, **kwargs):
        """
        查看增加页面
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.request = request

        popup = self.request.GET.get('_popup')
        if request.method == "GET":

            form = self.get_model_form_class()()
            context = {
                'form': form
            }
            # 因为页面内容需求不一，popup与正常add换转不同的页面
            if popup:
                return render(request, 'nb_lc/add_popup.html', context)
            else:
                return render(request, 'nb_lc/add.html', context)

        elif request.method == "POST":
            form = self.get_model_form_class()(data=request.POST)
            if form.is_valid():
                obj = form.save()  # ！！！获得form对象
                obj_id = obj.pk  # 对象id
                text = str(obj)  # 对象内容
                context = {"text": text, "obj_pk": obj_id, "popup": popup}
                if popup:
                    return render(request, 'nb_lc/popup_ready.html', context)
                else:
                    # 跳转回change_list页面
                    change_list_url_params = request.GET.get('_xxxxxxxxxxxx')
                    # print(change_list_url_params)
                    base_url = self.reverse_change_list_url()
                    url = "%s?%s" % (base_url, change_list_url_params,)
                    return redirect(url)

            context = {
                'form': form
            }
            return render(request, 'nb_lc/add.html', context)

    def delete_view(self, request, *args, **kwargs):
        return HttpResponse('删除页面')

    def change_view(self, request, pk, *args, **kwargs):
        # 获取对象
        obj = self.model_class.objects.filter(pk=pk).first()

        if request.method == "GET":
            form = self.get_model_form_class()(instance=obj)

            context = {
                'form': form
            }
            return render(request, 'nb_lc/change.html', context)
        elif request.method == "POST":
            form = self.get_model_form_class()(data=request.POST, instance=obj)
            if form.is_valid():
                form.save()
                return redirect(self.reverse_change_list_url())
            context = {
                'form': form
            }
            return render(request, 'nb_lc/change.html', context)

    def reverse_change_list_url(self):
        url = reverse("%s:%s_%s_changelist" % (self.site.namespace, self.app_label, self.model_name,))
        return url

    def get_urls(self):
        from django.conf.urls import url

        app_model_name = self.model_class._meta.app_label, self.model_class._meta.model_name

        patterns = [
            url(r'^$', self.changelist_view, name="%s_%s_changelist" % (app_model_name)),
            url(r'^add/$', self.add_view, name="%s_%s_add" % (app_model_name)),
            url(r'^(.+)/delete/$', self.delete_view, name="%s_%s_delete" % (app_model_name)),
            url(r'^(.+)/change/$', self.change_view, name="%s_%s_change" % (app_model_name)),
        ]

        patterns += self.extra_urls()
        return patterns

    def extra_urls(self):
        """
        扩展URL预留的钩子函数
        :return:
        """
        return []

    @property
    def urls(self):
        return self.get_urls(), None, None


class NbSite(object):
    """
    site类
    """

    def __init__(self):
        self.name = 'nb'
        self.namespace = 'nb'
        self._registry = {}

    def register(self, model, model_nb=None):
        if not model_nb:
            model_nb = ModelNb
        self._registry[model] = model_nb(model, self)
        print(self._registry)

    def login(self, request):

        return HttpResponse('登录页面')

    def logout(self, request):
        return HttpResponse('注销页面')

    def get_urls(self):
        patterns = []

        from django.conf.urls import url, include
        patterns += [
            url(r'^login/', self.login),
            url(r'^logout/', self.logout),
        ]

        for model_class, model_nb_obj in self._registry.items():
            patterns += [
                url(r'^%s/%s/' % (model_class._meta.app_label, model_class._meta.model_name,), model_nb_obj.urls)
            ]

        return patterns

    @property
    def urls(self):
        return self.get_urls(), self.name, self.namespace


site = NbSite()
