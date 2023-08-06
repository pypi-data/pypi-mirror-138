from . import deepwalk, snn, feature, links, utils, layers

__all__ = ['deepwalk', 'snn', 'feature', 'links', 'utils']

desc = {'deepwalk': 'deepwalk that accept sp.csr_matrix',
        'snn': "spiking neurons",
        'feature': "feature engineering, xgboost, lightgbm, catboost, rf",
        'links': ' some links available during competition',
        'utils': 'lrscheduler, loss',
        'layers': 'layers'}
