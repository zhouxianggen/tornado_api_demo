# coding: utf8 
import os
import re
from importlib.util import spec_from_loader,module_from_spec
from importlib.machinery import SourceFileLoader
from tornado_api_demo.errors import ApiError
from tornado_api_demo.util import get_logger


class Factory(object):
    def __init__(self):
        self.log = get_logger('Factory')
        self.impls = {}


    def init(self):
        cwd = os.path.dirname(os.path.abspath(__file__))
        reo = re.compile(r'(v(\w+))$', re.I)
        for sub in os.listdir(cwd):
            subdir = os.path.join(cwd, sub)
            if not os.path.isdir(subdir):
                continue
            m = reo.match(sub)
            if not m:
                continue
            name, version = m.group(1), m.group(2)
            mfile = os.path.join(subdir, 'model.py')
            if not os.path.isfile(mfile):
                continue
            self.log.info('load model impl {}'.format(version))
            name = 'v{}.py'.format(version)
            loader = SourceFileLoader(name, mfile)
            spec = spec_from_loader(loader.name, loader)
            mod = module_from_spec(spec)
            loader.exec_module(mod)
            self.impls[version] = mod.Model


    def gen(self, version):
        if version not in self.impls:
            raise ApiError('version {} not implemented'.format(version))
        return self.impls[version]()

