"""
This module enables installing and importing any PyPI package simply by:

    from pypi import packagename

Use underscore instead of dash, if found in package name. When package contains multiple
top-level modules it attempts to choose the most similar to the name of the package itself.

Note: does not support "import pypi.something" or "import pypi.something as somethingelse"
"""


class FromPyPI:
    def __init__(self):
        from pip._vendor.distlib.database import DistributionPath
        import logging
        logging.getLogger('pip._vendor.distlib.metadata').setLevel(logging.ERROR)
        self.index = DistributionPath()

    def get_pip_module(self, name):
        distname = name.replace('_', '-')
        dist = self.index.get_distribution(distname)
        if dist is None:
            if not self.pip_install(distname):
                raise ModuleNotFoundError(name)
            self.index.clear_cache()
        dist = self.index.get_distribution(distname)
        if dist is None:
            raise ImportError('Huh? Successfully installed package but cannot find it')
        if not dist.modules:
            raise ImportError('Package has no top level modules')
        dist.modules = [m.decode() if type(m) is bytes else m for m in dist.modules]
        modname = self.choose(name, dist.modules)
        return __import__(modname)

    def choose(self, name, candidates):
        # Packages may have multiple top level modules, and package name
        # may not exactly match any of the top level module names

        def score(candidate):
            n = set(name.lower())
            c = set(candidate.lower())
            return 100.0 * len(c & n) / max(len(c), len(n))

        return sorted(candidates, key=score)[-1]

    def pip_install(self, distname):
        import sys, subprocess
        return 0 == subprocess.call([
            sys.executable, '-m', 'pip', 'install', '--prefer-binary', distname
        ])

    def entrypoint(self, name):
        if name == '__check':
            return 'ok'
        if name.startswith('__'):
            raise AttributeError(name)
        return self.get_pip_module(name)


__getattr__ = FromPyPI().entrypoint


def module_getattr_workaround():
    # For pre PEP562 python (< 3.7)
    from sys import modules
    thismod = modules[__name__]
    assert vars(thismod) is globals()
    del thismod.module_getattr_workaround

    if getattr(thismod, '__check', None) == 'ok':
        return

    class module(type(thismod)):
        def __getattr__(self, name):
            return self.__dict__['__getattr__'](name)

    newmod = module(__name__)
    vars(newmod).update(vars(thismod))
    modules[__name__] = newmod

module_getattr_workaround()
