# -*- coding: utf-8 -*-

import importlib


def load_module(module_path, module_class, *args, **kwargs):
    """
    Helper function to dynamically load modules based on user input/config
    """
    module = importlib.import_module(module_path)
    class_ = getattr(module, module_class)
    return class_(*args, **kwargs)