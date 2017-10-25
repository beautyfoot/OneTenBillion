from django.template.library import Library
from types import FunctionType

register = Library()


@register.inclusion_tag('nb_lc/change_list_table.html')
def show_result_list(cl):
    def headers():
        if not cl.list_display:
            yield cl.model_config_obj.model_class._meta.model_name
        else:
            for v in cl.list_display:
                yield v(cl.model_config_obj, is_header=True) if isinstance(v,
                                                                           FunctionType) else cl.model_config_obj.model_class._meta.get_field(
                    v).verbose_name

    def body():
        for row in cl.data_list:
            if not cl.list_display:
                yield [str(row), ]
            else:
                yield [name(cl.model_config_obj, obj=row) if isinstance(name, FunctionType) else  getattr(row, name) for
                       name in
                       cl.list_display]

    return {'headers': headers(),
            'body': body(), }


@register.inclusion_tag('nb_lc/change_list_actions.html')
def show_actions(cl):
    def func(cl):
        for item in cl.actions:
            yield (item.__name__, item.short_desc,)

    return {"actions": func(cl)}
