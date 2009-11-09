from distutils.core import setup
import py2exe

setup(
        windows=[{'script':'wiki.pyw', 'icon_resources': [(1, "wiki.ico")]}],
    #console=['exe.py'],
    #data_files=[
    #    ("", ["config-example.ini"])
    #]
)

