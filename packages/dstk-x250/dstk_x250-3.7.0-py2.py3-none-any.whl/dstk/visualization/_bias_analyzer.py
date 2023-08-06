#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe Scikit-Learn like pour analyser les biais d'une modélisation.

Created on Sun Feb 13 14:52:34 2022

@author: Cyrile Delestre
"""

from dataclasses import dataclass, field
from typing import List, Optional, Union
from itertools import product, chain
from collections import OrderedDict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.metrics import (roc_auc_score, accuracy_score, f1_score,
                             matthews_corrcoef)
from joblib import Parallel, delayed
from tqdm import tqdm


@dataclass
class BiasAnalyser(BaseEstimator, TransformerMixin):
    score = dict(
        acc=accuracy_score,
        f1=f1_score,
        roc_auc=roc_auc_score,
        mcc=matthews_corrcoef
    )
    degre: int = 1

    def fit(
        self,
        X: pd.DataFrame,
        y: Optional[Union[np.ndarray, pd.DataFrame]]=None,
        labels: Optional[List[str]]=None
    ):
        return self

    def transform(
    ):
        ...
