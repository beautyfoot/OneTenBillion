from django.apps import AppConfig

class NbLcConfig(AppConfig):
    name = 'nb_lc'

    def ready(self):
        """
        启动之前取所有app里找nbLc.py
        :return:
        """
        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('nbLc')

