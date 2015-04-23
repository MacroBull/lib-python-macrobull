from distutils.core import setup, Extension
setup(name="core", version="1.0",
                ext_modules=[Extension("core", ["core.c"])])