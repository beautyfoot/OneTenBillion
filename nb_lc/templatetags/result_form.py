from django.forms import ModelChoiceField
from django.template.library import Library
from django.urls import reverse

from nb_lc.service.nb import site

register = Library()


def upForm(model_form_obj):
    for item in model_form_obj:
        tpl = {'has_popup': False, 'item': item, 'popup_url': None}
        # 通过判断是否是ModelChoiceField类型，且被注册的Model，添加popup
        if isinstance(item.field, ModelChoiceField) and item.field.queryset.model in site._registry:
            tpl['has_popup'] = True
            # 反向生成url
            field_class = item.field.queryset.model  # 类名
            # print('field_class^^^^^^^', field_class)  # <class 'app01.models.UserGroup'><class 'app01.models.Role'>
            app_label = field_class._meta.app_label  # app名字
            model_name = field_class._meta.model_name  # 模块名字
            url = reverse('{0}:{1}_{2}_add'.format(site.namespace, app_label, model_name))
            url = "{0}?_popup={1}".format(url, item.auto_id)
            tpl['popup_url'] = url

        yield tpl


@register.inclusion_tag('nb_lc/add_form.html')
def show_form(model_form_obj):
    return {"form": upForm(model_form_obj)}
