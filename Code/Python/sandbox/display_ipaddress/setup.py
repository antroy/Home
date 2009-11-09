from distutils.core import setup
import py2exe

setup(
    windows=[
        {
            "script": 'ip-address.py',
            "icon_resources": [(1, "ip.ico")]
        }
    ],
)

