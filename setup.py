import re
import os

from setuptools import setup


version = ''
with open('neofetch_win/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)


if not version:
    raise RuntimeError('version is not set')

if os.name != "nt":
    raise RuntimeError('You can only install this on Windows, sorry.')


setup(
    name='neofetch-win',
    author='AlexFlipnote',
    url='https://github.com/AlexFlipnote/neofetch-win',
    version=version,
    packages=['neofetch_win'],
    license='GNU v3',
    description='neofetch, but for Windows',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'neofetch=neofetch_win.main:main'
        ]
    }
)
