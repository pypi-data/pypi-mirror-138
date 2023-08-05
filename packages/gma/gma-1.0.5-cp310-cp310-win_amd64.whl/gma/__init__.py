# -*- coding: utf-8 -*-

try:
    from . import index, math, osf, rasp, vesp, smc

except ModuleNotFoundError as F:

    Package = str(F).split()[-1].replace("'",'').split('.')[0]
    if Package == 'osgeo':
        MESS = "缺少 gdal 库，gdal 的 whl 包下载地址：https://www.lfd.uci.edu/~gohlke/pythonlibs/"
    else:
        MESS = f"缺少 {Package} 库，请在终端使用 'pip install {Package}' 安装！"

    raise ModuleNotFoundError(MESS) from None

except ImportError as I:

    Module = str(I).split()

    if 'from' in Module:
        LOC = Module.index('from')

        raise ImportError(f'无法从 {Module[LOC+1]} 中导入 {Module[LOC-1]}！') from None

    else:
        raise ImportError('父包未知，无法进行相对导入！') from None

