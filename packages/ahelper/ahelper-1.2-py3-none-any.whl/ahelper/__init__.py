from . import deepwalk, snn, feature, links, utils, layers

__all__ = ['deepwalk', 'snn', 'feature', 'links', 'utils']

desc = {'deepwalk': 'deepwalk that accept sp.csr_matrix',
        'snn': "spiking neurons",
        'feature': "feature engineering, xgboost, lightgbm, catboost, rf",
        'links': ' some links available during competition',
        'utils': 'lrscheduler, loss',
        'layers': 'layers'}


rename = """
import os

fileList=os.listdir('.')

for i in fileList:
    #设置旧文件名（就是路径+文件名）
    if not i.endswith('.txt'): continue
    oldname=i
    
    newname=i[:-4]
    os.rename(oldname,newname)   #用os模块中的rename方法对文件改名
    print(oldname,'======>',newname)
"""