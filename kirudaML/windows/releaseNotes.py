# -*- coding: utf-8 -*-
from setuptools import setup
import py2exe
import sys

# name, description, version등의 정보는 일반적인 setup.py와 같습니다.

sys.path.append('dist')
sys.path.append("D:/GitHub/KirudaML/KirudaML")
#sys.path.append("C:/python27/lib/site-packages")
setup(name="kirudaML",
      description="kirudaML data stack program",
      version="1.0.0",
      windows=[{"script": "kirudaML.py"}],
      zipfile = None,
      options={
          'py2exe': {
              'bundle_files': 1, 
              'includes' : ['sip','PyQt4','kiruda.stack.stackData',],
              'packages': ['kirudaML','MySQLdb', ],
              # PySide 구동에 필요한 모듈들은 포함시켜줍니다.
              #=================================================================
              # "includes": ["PySide.QtCore",
              #              "PySide.QtGui",
              #              "PySide.QtWebKit",
              #              "PySide.QtNetwork",
              #              "PySide.QtXml"],
              #=================================================================
              # 존재하지 않거나 불필요한 파일은 제거합니다.
              #=================================================================
              # "dll_excludes": ["msvcr71.dll",
              #                  "MSVCP90.dll"],
              #=================================================================
          }
      })